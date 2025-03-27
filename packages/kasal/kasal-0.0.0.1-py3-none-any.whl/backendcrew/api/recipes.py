from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import inspect
import yaml
from ..database import get_db, Recipe, engine, Base
import logging

router = APIRouter()

logger = logging.getLogger(__name__)

def ensure_table_exists():
    """Ensure the recipes table exists in the database"""
    inspector = inspect(engine)
    if not inspector.has_table("recipes"):
        try:
            Base.metadata.create_all(bind=engine, tables=[Recipe.__table__])
            return True
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create recipes table: {str(e)}"
            )
    return False

@router.get("/")
async def get_all_recipes(db: Session = Depends(get_db)):
    """Get all available recipes"""
    ensure_table_exists()  # Ensure table exists
    recipes = db.query(Recipe).all()
    return [
        {
            "id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "iconName": recipe.icon_name,
            "color": recipe.color,
            "agents": recipe.agents,
            "difficulty": recipe.difficulty
        }
        for recipe in recipes
    ]

@router.get("/{recipe_id}")
async def get_recipe(recipe_id: str, db: Session = Depends(get_db)):
    """Get recipe configuration by ID"""
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail=f"Recipe not found: {recipe_id}")
    
    try:
        return {
            "id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "iconName": recipe.icon_name,
            "color": recipe.color,
            "agents": recipe.agents,
            "difficulty": recipe.difficulty,
            "config": {
                "agents_yaml": recipe.agents_yaml,
                "tasks_yaml": recipe.tasks_yaml
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving recipe: {str(e)}"
        )

@router.post("/")
async def create_recipe(recipe_data: dict, db: Session = Depends(get_db)):
    """Create a new recipe"""
    ensure_table_exists()  # Ensure table exists
    
    try:
        logger.info(f"Creating new recipe with data: {recipe_data}")
        
        # Validate and convert agents and tasks to YAML
        try:
            agents_yaml = yaml.dump(recipe_data.get('config', {}).get('agents', []))
            tasks_yaml = yaml.dump(recipe_data.get('config', {}).get('tasks', []))
            
            # Validate the YAML by attempting to load it back
            yaml.safe_load(agents_yaml)
            yaml.safe_load(tasks_yaml)
            
        except yaml.YAMLError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid YAML format in configuration: {str(e)}"
            )
        
        logger.info(f"Converted YAML - agents: {agents_yaml}, tasks: {tasks_yaml}")
        
        # Create new recipe instance
        recipe = Recipe(
            id=recipe_data['id'],
            title=recipe_data['title'],
            description=recipe_data['description'],
            icon_name=recipe_data['iconName'],
            color=recipe_data['color'],
            agents=recipe_data['agents'],
            difficulty=recipe_data['difficulty'],
            agents_yaml=agents_yaml,
            tasks_yaml=tasks_yaml
        )
        
        logger.info("Adding recipe to database session")
        db.add(recipe)
        
        logger.info("Committing to database")
        db.commit()
        
        logger.info("Refreshing recipe object")
        db.refresh(recipe)
        
        return {
            "recipe": {
                "id": recipe.id,
                "title": recipe.title,
                "description": recipe.description,
                "iconName": recipe.icon_name,
                "color": recipe.color,
                "agents": recipe.agents,
                "difficulty": recipe.difficulty
            },
            "config": {
                "agents": yaml.safe_load(recipe.agents_yaml) if recipe.agents_yaml else [],
                "tasks": yaml.safe_load(recipe.tasks_yaml) if recipe.tasks_yaml else []
            }
        }
        
    except Exception as e:
        logger.error(f"Error creating recipe: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=400, 
            detail=f"Failed to create recipe: {str(e)}"
        )

@router.delete("/{recipe_id}")
async def delete_recipe(recipe_id: str, db: Session = Depends(get_db)):
    """Delete a recipe by ID"""
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail=f"Recipe not found: {recipe_id}")
    
    try:
        db.delete(recipe)
        db.commit()
        return {"message": f"Recipe {recipe_id} deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting recipe: {str(e)}")

@router.put("/{recipe_id}")
async def update_recipe(recipe_id: str, recipe_data: dict, db: Session = Depends(get_db)):
    """Update an existing recipe"""
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail=f"Recipe not found: {recipe_id}")
    
    try:
        # Validate YAML format
        if 'agents_yaml' in recipe_data:
            yaml.safe_load(recipe_data['agents_yaml'])
        if 'tasks_yaml' in recipe_data:
            yaml.safe_load(recipe_data['tasks_yaml'])
            
        # Update recipe attributes
        recipe.title = recipe_data['title']
        recipe.description = recipe_data['description']
        recipe.icon_name = recipe_data['iconName']
        recipe.difficulty = recipe_data['difficulty']
        recipe.agents_yaml = recipe_data.get('agents_yaml', recipe.agents_yaml)
        recipe.tasks_yaml = recipe_data.get('tasks_yaml', recipe.tasks_yaml)
            
        db.commit()
        db.refresh(recipe)
        
        return {
            "id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "iconName": recipe.icon_name,
            "color": recipe.color,
            "agents": recipe.agents,
            "difficulty": recipe.difficulty
        }
        
    except yaml.YAMLError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Invalid YAML format: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Failed to update recipe: {str(e)}"
        )