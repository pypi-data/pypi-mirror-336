from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import croniter
import asyncio
from .. import database
from ..database import AsyncSessionLocal
from ..utils.job_runner import prepare_and_run_crew, jobs, JobStatus
from .jobs import CrewConfig
from .generate_job_name import generate_run_name
from ..utils.logger_manager import LoggerManager
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..callbacks import JobOutputCallback

router = APIRouter()
logger_manager = LoggerManager()

class ScheduleBase(BaseModel):
    name: str
    cron_expression: str
    agents_yaml: dict
    tasks_yaml: dict
    inputs: Optional[dict] = {}
    is_active: Optional[bool] = True
    planning: Optional[bool] = False
    model: Optional[str] = "gpt-4o-mini"

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleResponse(ScheduleBase):
    id: int
    last_run_at: Optional[datetime]
    next_run_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

def ensure_utc(dt: Optional[datetime]) -> Optional[datetime]:
    """Ensure a datetime is timezone-aware in UTC."""
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)

def calculate_next_run(cron_expression: str, base_time: Optional[datetime] = None) -> datetime:
    """Calculate the next run time for a cron expression."""
    if base_time is None:
        base_time = datetime.now()
    elif base_time.tzinfo is not None:
        base_time = base_time.astimezone().replace(tzinfo=None)
    
    try:
        cron = croniter.croniter(cron_expression, base_time)
        next_run = cron.get_next(datetime)
        local_tz = datetime.now().astimezone().tzinfo
        next_run_local = next_run.replace(tzinfo=local_tz)
        next_run_utc = next_run_local.astimezone(timezone.utc)
        logger_manager.scheduler.info(f"Calculated next run time: {next_run} (naive) -> {next_run_local} (local) -> {next_run_utc} (UTC)")
        return next_run_utc
    except Exception as e:
        logger_manager.scheduler.error(f"Error in calculate_next_run: {e}")
        raise

def calculate_next_run_from_last(cron_expression: str, last_run: Optional[datetime] = None) -> datetime:
    """Calculate the next run time from the last run time."""
    now = datetime.now()
    now_utc = datetime.now(timezone.utc)
    local_tz = now.astimezone().tzinfo
    
    if last_run is not None and last_run.tzinfo is not None:
        last_run = last_run.astimezone(local_tz).replace(tzinfo=None)
    
    logger_manager.scheduler.info(f"Calculating next run from last. Last run: {last_run}, Now (local): {now}, Now (UTC): {now_utc}")
    
    if last_run is None or last_run < now:
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        try:
            cron = croniter.croniter(cron_expression, today_start)
            next_run = cron.get_next(datetime)
            
            next_run_local = next_run.replace(tzinfo=local_tz)
            next_run_utc = next_run_local.astimezone(timezone.utc)
            
            if next_run.date() == now.date() and next_run > now:
                logger_manager.scheduler.info(f"Found next run time today: {next_run} (naive) -> {next_run_local} (local) -> {next_run_utc} (UTC)")
                return next_run_utc
                
            logger_manager.scheduler.info(f"No more runs today, calculating from now: {now}")
            return calculate_next_run(cron_expression, now)
            
        except Exception as e:
            logger_manager.scheduler.error(f"Error calculating next run time: {e}")
            return calculate_next_run(cron_expression, now)
    
    return calculate_next_run(cron_expression, last_run)

@router.post("", response_model=ScheduleResponse)
async def create_schedule(schedule: ScheduleCreate, db: AsyncSession = Depends(database.get_async_db)):
    try:
        # Calculate next run time
        next_run = calculate_next_run_from_last(schedule.cron_expression)
        
        # Create schedule record
        db_schedule = database.Schedule(
            name=schedule.name,
            cron_expression=schedule.cron_expression,
            agents_yaml=schedule.agents_yaml,
            tasks_yaml=schedule.tasks_yaml,
            inputs=schedule.inputs,
            is_active=schedule.is_active,
            next_run_at=next_run,
            planning=schedule.planning,
            model=schedule.model
        )
        db.add(db_schedule)
        await db.commit()
        await db.refresh(db_schedule)
        
        return db_schedule
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=List[ScheduleResponse])
async def list_schedules(db: AsyncSession = Depends(database.get_async_db)):
    stmt = select(database.Schedule)
    result = await db.execute(stmt)
    schedules = result.scalars().all()
    return schedules

@router.get("/{schedule_id}", response_model=ScheduleResponse)
async def get_schedule(schedule_id: int, db: AsyncSession = Depends(database.get_async_db)):
    stmt = select(database.Schedule).where(database.Schedule.id == schedule_id)
    result = await db.execute(stmt)
    schedule = result.scalar_one_or_none()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule

@router.put("/{schedule_id}", response_model=ScheduleResponse)
async def update_schedule(
    schedule_id: int,
    schedule_update: ScheduleCreate,
    db: AsyncSession = Depends(database.get_async_db)
):
    stmt = select(database.Schedule).where(database.Schedule.id == schedule_id)
    result = await db.execute(stmt)
    db_schedule = result.scalar_one_or_none()
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    # Update fields
    for field, value in schedule_update.dict().items():
        setattr(db_schedule, field, value)
    
    # Recalculate next run time from last run
    db_schedule.next_run_at = calculate_next_run_from_last(
        schedule_update.cron_expression,
        db_schedule.last_run_at
    )
    
    await db.commit()
    await db.refresh(db_schedule)
    return db_schedule

@router.delete("/{schedule_id}")
async def delete_schedule(schedule_id: int, db: AsyncSession = Depends(database.get_async_db)):
    stmt = select(database.Schedule).where(database.Schedule.id == schedule_id)
    result = await db.execute(stmt)
    db_schedule = result.scalar_one_or_none()
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    await db.delete(db_schedule)
    await db.commit()
    return {"message": "Schedule deleted successfully"}

@router.post("/{schedule_id}/toggle", response_model=ScheduleResponse)
async def toggle_schedule(schedule_id: int, db: AsyncSession = Depends(database.get_async_db)):
    stmt = select(database.Schedule).where(database.Schedule.id == schedule_id)
    result = await db.execute(stmt)
    db_schedule = result.scalar_one_or_none()
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    db_schedule.is_active = not db_schedule.is_active
    if db_schedule.is_active:
        db_schedule.next_run_at = calculate_next_run(db_schedule.cron_expression)
    
    await db.commit()
    await db.refresh(db_schedule)
    return db_schedule

async def run_schedule_job(schedule_id: int, config: CrewConfig, now: datetime):
    """Run a single schedule job in its own task."""
    try:
        sync_engine = create_engine(f'sqlite:///{database.DB_PATH}')
        SessionLocal = sessionmaker(bind=sync_engine)
        db = SessionLocal()
        
        try:
            job_id = str(uuid.uuid4())
            model = config.model or "gpt-3.5-turbo"
            run_name = await generate_run_name(config.agents_yaml, config.tasks_yaml, model, db)
            
            config_dict = {
                "agents_yaml": config.agents_yaml,
                "tasks_yaml": config.tasks_yaml,
                "inputs": config.inputs,
                "model": config.model
            }
            
            db_run = database.Run(
                job_id=job_id,
                status="pending",
                inputs=config_dict,
                created_at=now,
                trigger_type="scheduled",
                planning=config.planning,
                run_name=run_name
            )
            db.add(db_run)
            db.commit()
            
            jobs[job_id] = {
                "job_id": job_id,
                "status": JobStatus.PENDING.value,
                "created_at": now,
                "result": None,
                "error": None,
                "run_name": run_name
            }
            
            # Create streaming callback for the scheduled job
            streaming_cb = JobOutputCallback(job_id=job_id, max_retries=3)
            
            await prepare_and_run_crew(job_id, config, db, streaming_cb)
            
            async with AsyncSessionLocal() as schedule_session:
                stmt = select(database.Schedule).where(database.Schedule.id == schedule_id)
                result = await schedule_session.execute(stmt)
                schedule = result.scalar_one_or_none()
                
                if schedule:
                    schedule.last_run_at = now
                    schedule.next_run_at = calculate_next_run_from_last(
                        schedule.cron_expression,
                        now
                    )
                    await schedule_session.commit()
                    
                    logger_manager.scheduler.info(
                        f"Successfully ran schedule {schedule_id}."
                        f" Next run at: {schedule.next_run_at}"
                    )
        finally:
            db.close()
            
    except Exception as job_error:
        logger_manager.scheduler.error(f"Error running job for schedule {schedule_id}: {job_error}")
        try:
            async with AsyncSessionLocal() as error_session:
                stmt = select(database.Schedule).where(database.Schedule.id == schedule_id)
                result = await error_session.execute(stmt)
                schedule = result.scalar_one_or_none()
                
                if schedule:
                    schedule.last_run_at = now
                    schedule.next_run_at = calculate_next_run_from_last(
                        schedule.cron_expression,
                        now
                    )
                    await error_session.commit()
        except Exception as update_error:
            logger_manager.scheduler.error(f"Error updating schedule {schedule_id} after job failure: {update_error}")

async def check_and_run_schedules(db: AsyncSession):
    logger_manager.scheduler.info("Schedule checker started and running")
    running_tasks = set()
    
    while True:
        try:
            running_tasks = {task for task in running_tasks if not task.done()}
            
            now_utc = datetime.now(timezone.utc)
            now_local = datetime.now().astimezone()
            logger_manager.scheduler.info(f"Checking for due schedules at {now_local} (local) / {now_utc} (UTC)")
            logger_manager.scheduler.info(f"Currently running tasks: {len(running_tasks)}")
            
            async with AsyncSessionLocal() as session:
                stmt = select(database.Schedule).where(
                    database.Schedule.is_active == True,
                    database.Schedule.next_run_at <= now_utc
                )
                result = await session.execute(stmt)
                due_schedules = result.scalars().all()
                
                all_stmt = select(database.Schedule)
                all_result = await session.execute(all_stmt)
                all_schedules = all_result.scalars().all()
                
                logger_manager.scheduler.info("Current schedules status:")
                for schedule in all_schedules:
                    next_run = ensure_utc(schedule.next_run_at)
                    last_run = ensure_utc(schedule.last_run_at)
                    is_due = schedule.is_active and next_run is not None and next_run <= now_utc
                    
                    next_run_local = next_run.astimezone() if next_run else None
                    last_run_local = last_run.astimezone() if last_run else None
                    
                    logger_manager.scheduler.info(
                        f"Schedule {schedule.id} - {schedule.name}:"
                        f" active={schedule.is_active},"
                        f" next_run={next_run_local} (local) / {next_run} (UTC),"
                        f" last_run={last_run_local} (local) / {last_run} (UTC),"
                        f" cron={schedule.cron_expression},"
                        f" planning={schedule.planning},"
                        f" model={schedule.model},"
                        f" is_due={is_due}"
                        f" (now={now_local} local / {now_utc} UTC)"
                    )
                
                logger_manager.scheduler.info(f"Found {len(due_schedules)} schedules due to run")
                
                for schedule in due_schedules:
                    logger_manager.scheduler.info(f"Starting task for schedule {schedule.id} - {schedule.name}")
                    logger_manager.scheduler.info(f"Schedule configuration: agents_yaml={schedule.agents_yaml}, tasks_yaml={schedule.tasks_yaml}, inputs={schedule.inputs}, planning={schedule.planning}, model={schedule.model}")
                    config = CrewConfig(
                        agents_yaml=schedule.agents_yaml,
                        tasks_yaml=schedule.tasks_yaml,
                        inputs=schedule.inputs,
                        planning=schedule.planning,
                        model=schedule.model
                    )
                    
                    task = asyncio.create_task(
                        run_schedule_job(schedule.id, config, now_utc),
                        name=f"schedule_{schedule.id}_{now_utc.isoformat()}"
                    )
                    running_tasks.add(task)
                    
                    schedule.next_run_at = calculate_next_run_from_last(
                        schedule.cron_expression,
                        now_utc
                    )
                    await session.commit()
            
            for task in running_tasks:
                if task.done():
                    try:
                        await task
                    except Exception as e:
                        logger_manager.scheduler.error(f"Task {task.get_name()} failed with error: {e}")
            
            logger_manager.scheduler.info("Sleeping for 60 seconds before next check")
            await asyncio.sleep(60)
        except Exception as e:
            logger_manager.scheduler.error(f"Error in schedule checker: {e}")
            await asyncio.sleep(60)
