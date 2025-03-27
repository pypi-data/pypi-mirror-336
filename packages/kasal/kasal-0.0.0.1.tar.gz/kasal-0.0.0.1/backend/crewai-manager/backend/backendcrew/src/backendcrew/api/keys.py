import os
import logging
import aiohttp
import base64
from typing import List, Optional
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from pathlib import Path
from .databricks import get_active_config
from ..database import get_async_db, ApiKey

logger = logging.getLogger(__name__)
router = APIRouter()

# Models
class SecretUpdate(BaseModel):
    value: str
    description: str = ""

class SecretCreate(BaseModel):
    name: str
    value: str
    description: str = ""

class SecretResponse(BaseModel):
    id: int
    name: str
    value: str
    description: str
    scope: str
    source: str = "databricks"  # 'databricks' or 'sqlite'

class DatabricksTokenRequest(BaseModel):
    workspace_url: str
    token: str

# Encryption utilities
def get_key_directory() -> Path:
    """Get the directory where SSH keys are stored"""
    # Use a directory in the user's home directory
    home_dir = Path.home()
    key_dir = home_dir / ".backendcrew" / "keys"
    key_dir.mkdir(parents=True, exist_ok=True)
    return key_dir

def generate_ssh_key_pair() -> tuple[bytes, bytes]:
    """Generate a new RSA key pair for encryption"""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # Serialize private key
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Serialize public key
    public_key_bytes = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    return private_key_bytes, public_key_bytes

def get_or_create_ssh_keys() -> tuple[bytes, bytes]:
    """Get existing SSH keys or create new ones if they don't exist"""
    key_dir = get_key_directory()
    private_key_path = key_dir / "private_key.pem"
    public_key_path = key_dir / "public_key.pem"
    
    # Check if keys already exist
    if private_key_path.exists() and public_key_path.exists():
        private_key = private_key_path.read_bytes()
        public_key = public_key_path.read_bytes()
    else:
        # Generate new keys
        private_key, public_key = generate_ssh_key_pair()
        # Save keys to files
        private_key_path.write_bytes(private_key)
        public_key_path.write_bytes(public_key)
        logger.info("Generated new SSH key pair for encryption")
    
    return private_key, public_key

def get_encryption_key() -> bytes:
    """Get or generate a Fernet encryption key (for backward compatibility)"""
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        # Generate a key and warn that it's not persisted
        key = Fernet.generate_key().decode()
        logger.warning(
            "ENCRYPTION_KEY environment variable not set. "
            "Generated a temporary key. Keys will not persist across restarts."
        )
    return key.encode() if isinstance(key, str) else key

def encrypt_with_ssh(value: str) -> str:
    """Encrypt a value using RSA public key encryption"""
    try:
        _, public_key_bytes = get_or_create_ssh_keys()
        public_key = serialization.load_pem_public_key(
            public_key_bytes,
            backend=default_backend()
        )
        
        # RSA can only encrypt limited data size, so we'll use a hybrid approach
        # Generate a symmetric key
        symmetric_key = Fernet.generate_key()
        f = Fernet(symmetric_key)
        
        # Encrypt the value with the symmetric key
        encrypted_value = f.encrypt(value.encode())
        
        # Encrypt the symmetric key with the public key
        encrypted_key = public_key.encrypt(
            symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Combine the encrypted key and value, with a separator
        combined = base64.b64encode(encrypted_key) + b":" + encrypted_value
        return base64.b64encode(combined).decode()
    except Exception as e:
        logger.error(f"Error encrypting value with SSH key: {str(e)}")
        raise

def decrypt_with_ssh(encrypted_value: str) -> str:
    """Decrypt a value using RSA private key encryption"""
    try:
        private_key_bytes, _ = get_or_create_ssh_keys()
        private_key = serialization.load_pem_private_key(
            private_key_bytes,
            password=None,
            backend=default_backend()
        )
        
        # Decode the combined value
        combined = base64.b64decode(encrypted_value.encode())
        encrypted_key, encrypted_data = combined.split(b":", 1)
        encrypted_key = base64.b64decode(encrypted_key)
        
        # Decrypt the symmetric key
        symmetric_key = private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Use the symmetric key to decrypt the value
        f = Fernet(symmetric_key)
        decrypted_value = f.decrypt(encrypted_data).decode()
        return decrypted_value
    except Exception as e:
        logger.error(f"Error decrypting value with SSH key: {str(e)}")
        return ""

def is_ssh_encrypted(value: str) -> bool:
    """Check if a value is encrypted with SSH keys"""
    try:
        # Try to decode as base64 and split
        combined = base64.b64decode(value.encode())
        parts = combined.split(b":", 1)
        return len(parts) == 2
    except:
        return False

def encrypt_value(value: str) -> str:
    """Encrypt a value using SSH key encryption or Fernet for backward compatibility"""
    try:
        # Use SSH encryption
        return encrypt_with_ssh(value)
    except Exception as e:
        logger.error(f"Error with SSH encryption, falling back to Fernet: {str(e)}")
        # Fall back to Fernet encryption
        f = Fernet(get_encryption_key())
        return f.encrypt(value.encode()).decode()

def decrypt_value(encrypted_value: str) -> str:
    """Decrypt a value using the appropriate method"""
    try:
        if is_ssh_encrypted(encrypted_value):
            return decrypt_with_ssh(encrypted_value)
        else:
            # Use Fernet for backward compatibility
            f = Fernet(get_encryption_key())
            return f.decrypt(encrypted_value.encode()).decode()
    except Exception as e:
        logger.error(f"Error decrypting value: {str(e)}")
        return ""

# Core utility functions
async def validate_databricks_config(db: AsyncSession) -> tuple[str, str]:
    """Get Databricks configuration from database"""
    config = await get_active_config(db)
    if not config:
        raise ValueError("Databricks configuration not found")
    
    # Check if Databricks is enabled
    if hasattr(config, 'is_enabled') and not config.is_enabled:
        raise ValueError("Databricks integration is disabled")
    
    # Use a default workspace_url if not provided
    workspace_url = config.workspace_url or ""
    
    return workspace_url, config.secret_scope

async def create_secret_scope(db: AsyncSession, scope: str) -> bool:
    """Create a secret scope if it doesn't exist"""
    try:
        workspace_url, scope = await validate_databricks_config(db)
        token = os.getenv("DATABRICKS_TOKEN", "")  # Get token from environment variable
        
        # Skip if workspace_url is not provided
        if not workspace_url:
            logger.warning("Workspace URL not provided, skipping secret scope creation")
            return False
            
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{workspace_url}/api/2.0/secrets/scopes/create",
                headers={"Authorization": f"Bearer {token}"},
                json={"scope": scope, "initial_manage_principal": "users"}
            ) as response:
                if response.status == 200:
                    return True
                elif response.status == 400 and "RESOURCE_ALREADY_EXISTS" in await response.text():
                    return True
                return False
    except Exception as e:
        logger.error(f"Error creating secret scope: {str(e)}")
        return False

# Databricks secrets utility functions
async def get_databricks_secrets(db: AsyncSession, scope: str) -> Optional[List[dict]]:
    """Get all secrets from a specific Databricks scope"""
    try:
        token = os.getenv("DATABRICKS_TOKEN", "")  # Default to empty string if not set

        config = await get_active_config(db)
        if not config:
            logger.error("Databricks configuration not found")
            return None

        workspace_url = config.workspace_url
        
        # Skip if workspace_url is not provided
        if not workspace_url:
            logger.warning("Workspace URL not provided, skipping get_databricks_secrets")
            return None
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{workspace_url}/api/2.0/secrets/list",
                headers={"Authorization": f"Bearer {token}"},
                params={"scope": scope}
            ) as response:
                if response.status == 200:
                    return await response.json()
                return None
    except Exception as e:
        logger.error(f"Error getting secrets: {str(e)}")
        return None

async def set_secret_value(db: AsyncSession, scope: str, key: str, value: str) -> bool:
    """Set a secret value in Databricks"""
    try:
        token = os.getenv("DATABRICKS_TOKEN", "")  # Default to empty string if not set

        config = await get_active_config(db)
        if not config:
            raise ValueError("Databricks configuration not found")

        workspace_url = config.workspace_url
        
        # Skip if workspace_url is not provided
        if not workspace_url:
            logger.warning("Workspace URL not provided, skipping set_secret_value")
            return False
        
        # Ensure scope exists
        await create_secret_scope(db, scope)

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'{workspace_url}/api/2.0/secrets/put',
                headers={'Authorization': f'Bearer {token}'},
                json={
                    'scope': scope,
                    'key': key,
                    'string_value': value
                }
            ) as response:
                response.raise_for_status()
                return True
    except Exception as e:
        logger.error(f"Error setting secret value: {str(e)}")
        raise

async def delete_secret(db: AsyncSession, scope: str, key: str) -> bool:
    """Delete a secret from Databricks"""
    try:
        token = os.getenv("DATABRICKS_TOKEN", "")  # Default to empty string if not set

        config = await get_active_config(db)
        if not config:
            raise ValueError("Databricks configuration not found")

        workspace_url = config.workspace_url
        
        # Skip if workspace_url is not provided
        if not workspace_url:
            logger.warning("Workspace URL not provided, skipping delete_secret")
            return False

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'{workspace_url}/api/2.0/secrets/delete',
                headers={'Authorization': f'Bearer {token}'},
                json={
                    'scope': scope,
                    'key': key
                }
            ) as response:
                response.raise_for_status()
                return True
    except Exception as e:
        logger.error(f"Error deleting secret: {str(e)}")
        raise

async def get_secret_value(db: AsyncSession, scope: str, key: str) -> str:
    """Get a specific secret value from Databricks"""
    try:
        token = os.getenv("DATABRICKS_TOKEN", "")  # Default to empty string if not set

        config = await get_active_config(db)
        if not config:
            raise ValueError("Databricks configuration not found")

        workspace_url = config.workspace_url
        
        # Skip if workspace_url is not provided
        if not workspace_url:
            logger.warning("Workspace URL not provided, skipping get_secret_value")
            return ""

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'{workspace_url}/api/2.0/secrets/get',
                headers={'Authorization': f'Bearer {token}'},
                params={'scope': scope, 'key': key}
            ) as response:
                response.raise_for_status()
                data = await response.json()
                secret_value_encoded = data.get('value')
                return base64.b64decode(secret_value_encoded).decode('utf-8')
    except Exception as e:
        logger.error(f"Error getting secret value: {str(e)}")
        return ""

# SQLite API key utility functions
async def get_sqlite_api_keys(db: AsyncSession) -> List[dict]:
    """Get all API keys from SQLite database"""
    try:
        result = await db.execute(select(ApiKey))
        api_keys = result.scalars().all()
        
        formatted_keys = []
        for idx, key in enumerate(api_keys, 1):
            # Decrypt the value
            decrypted_value = decrypt_value(key.encrypted_value)
            formatted_keys.append({
                "id": key.id,
                "name": key.name,
                "value": decrypted_value,
                "description": key.description or "",
                "scope": "local",
                "source": "sqlite"
            })
        
        return formatted_keys
    except Exception as e:
        logger.error(f"Error getting API keys from SQLite: {str(e)}")
        return []

async def create_sqlite_api_key(db: AsyncSession, name: str, value: str, description: str = "") -> bool:
    """Create a new API key in SQLite database"""
    try:
        # Encrypt the value
        encrypted_value = encrypt_value(value)
        
        # Create new API key
        api_key = ApiKey(
            name=name,
            encrypted_value=encrypted_value,
            description=description
        )
        
        db.add(api_key)
        await db.commit()
        return True
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating API key in SQLite: {str(e)}")
        raise

async def update_sqlite_api_key(db: AsyncSession, name: str, value: str, description: str = "") -> bool:
    """Update an API key in SQLite database"""
    try:
        # Find the API key
        result = await db.execute(select(ApiKey).where(ApiKey.name == name))
        api_key = result.scalars().first()
        
        if not api_key:
            raise ValueError(f"API key '{name}' not found")
        
        # Update the API key
        api_key.encrypted_value = encrypt_value(value)
        if description:
            api_key.description = description
        
        await db.commit()
        return True
    except Exception as e:
        await db.rollback()
        logger.error(f"Error updating API key in SQLite: {str(e)}")
        raise

async def delete_sqlite_api_key(db: AsyncSession, name: str) -> bool:
    """Delete an API key from SQLite database"""
    try:
        # Delete the API key
        result = await db.execute(delete(ApiKey).where(ApiKey.name == name))
        await db.commit()
        
        if result.rowcount == 0:
            raise ValueError(f"API key '{name}' not found")
        
        return True
    except Exception as e:
        await db.rollback()
        logger.error(f"Error deleting API key from SQLite: {str(e)}")
        raise

async def get_sqlite_api_key(db: AsyncSession, name: str) -> Optional[dict]:
    """Get a specific API key from SQLite database"""
    try:
        result = await db.execute(select(ApiKey).where(ApiKey.name == name))
        api_key = result.scalars().first()
        
        if not api_key:
            return None
        
        # Decrypt the value
        decrypted_value = decrypt_value(api_key.encrypted_value)
        
        return {
            "id": api_key.id,
            "name": api_key.name,
            "value": decrypted_value,
            "description": api_key.description or "",
            "scope": "local",
            "source": "sqlite"
        }
    except Exception as e:
        logger.error(f"Error getting API key from SQLite: {str(e)}")
        return None

# API Routes
@router.get("/api-keys")
async def get_api_keys(db: AsyncSession = Depends(get_async_db), source: str = None):
    """Get all API keys from Databricks secrets and SQLite database"""
    try:
        # Get keys from SQLite if source is not specified or is 'sqlite'
        sqlite_keys = []
        if source is None or source == 'sqlite':
            sqlite_keys = await get_sqlite_api_keys(db)
        
        # Try to get keys from Databricks if configured and source is not specified or is 'databricks'
        databricks_keys = []
        if source is None or source == 'databricks':
            try:
                # Removed token check
                try:
                    workspace_url, scope = await validate_databricks_config(db)
                    secrets_response = await get_databricks_secrets(db, scope)
                    if secrets_response:
                        # Format secrets for response
                        secrets = secrets_response.get('secrets', [])
                        for idx, secret in enumerate(secrets, len(sqlite_keys) + 1):
                            # Get the secret value
                            secret_value = await get_secret_value(db, scope, secret.get('key'))
                            databricks_keys.append({
                                "id": idx,
                                "name": secret.get('key', ''),
                                "value": secret_value,
                                "description": "",  # Databricks API doesn't provide descriptions
                                "scope": scope,
                                "source": "databricks"
                            })
                except ValueError as ve:
                    # If Databricks is disabled, just log a warning and continue
                    logger.error(f"Configuration error: {str(ve)}")
            except Exception as e:
                logger.warning(f"Error getting Databricks API keys: {str(e)}")
                # Continue with SQLite keys only
        
        # Combine and return all keys
        return sqlite_keys + databricks_keys
    except Exception as e:
        logger.error(f"Error getting API keys: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting API keys: {str(e)}")

@router.post("/api-key")
async def create_api_key(secret: SecretCreate, db: AsyncSession = Depends(get_async_db)):
    """Create a new API key in SQLite database or Databricks secrets"""
    try:
        # Check if key already exists in SQLite
        existing_key = await get_sqlite_api_key(db, secret.name)
        if existing_key:
            raise ValueError(f"API key '{secret.name}' already exists in SQLite")
        
        # Try to store in SQLite first
        try:
            await create_sqlite_api_key(db, secret.name, secret.value, secret.description)
            return {"message": "Secret created successfully in SQLite"}
        except Exception as sqlite_error:
            logger.warning(f"Failed to create API key in SQLite: {str(sqlite_error)}")
            
            # Fall back to Databricks if available
            try:
                workspace_url, scope = await validate_databricks_config(db)
                await set_secret_value(db, scope, secret.name, secret.value)
                return {"message": "Secret created successfully in Databricks"}
            except Exception as databricks_error:
                logger.error(f"Failed to create API key in Databricks: {str(databricks_error)}")
                raise ValueError(f"Failed to create API key: {str(sqlite_error)}. Databricks fallback also failed: {str(databricks_error)}")
    except ValueError as ve:
        logger.error(f"Configuration error: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error creating API key: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error creating API key: {str(e)}")

@router.put("/api-keys/{key_name}")
async def update_api_key(key_name: str, secret: SecretUpdate, db: AsyncSession = Depends(get_async_db)):
    """Update an API key in SQLite database or Databricks secrets"""
    try:
        # Check if key exists in SQLite
        existing_key = await get_sqlite_api_key(db, key_name)
        
        if existing_key:
            # Update in SQLite
            await update_sqlite_api_key(db, key_name, secret.value, secret.description)
            return {"message": "Secret updated successfully in SQLite"}
        else:
            # Try to update in Databricks
            try:
                workspace_url, scope = await validate_databricks_config(db)
                await set_secret_value(db, scope, key_name, secret.value)
                return {"message": "Secret updated successfully in Databricks"}
            except Exception as e:
                logger.error(f"Error updating API key in Databricks: {str(e)}")
                raise
    except Exception as e:
        logger.error(f"Error updating API key: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating API key: {str(e)}")

@router.delete("/api-key/{key_name}")
async def delete_api_key(key_name: str, db: AsyncSession = Depends(get_async_db)):
    """Delete an API key from SQLite database or Databricks secrets"""
    try:
        # Check if key exists in SQLite
        existing_key = await get_sqlite_api_key(db, key_name)
        
        if existing_key:
            # Delete from SQLite
            await delete_sqlite_api_key(db, key_name)
            return {"message": "Secret deleted successfully from SQLite"}
        else:
            # Try to delete from Databricks
            try:
                workspace_url, scope = await validate_databricks_config(db)
                await delete_secret(db, scope, key_name)
                return {"message": "Secret deleted successfully from Databricks"}
            except Exception as e:
                logger.error(f"Error deleting API key from Databricks: {str(e)}")
                raise
    except Exception as e:
        logger.error(f"Error deleting API key: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting API key: {str(e)}")

# Legacy routes for backward compatibility
@router.post("/secret-scopes")
async def create_secret_scope_endpoint(db: AsyncSession = Depends(get_async_db)) -> bool:
    """Create a secret scope if it doesn't exist"""
    workspace_url, scope = await validate_databricks_config(db)
    return await create_secret_scope(db, scope)

@router.get("/secrets")
async def get_secrets(db: AsyncSession = Depends(get_async_db)):
    """Get all secrets from a specific Databricks scope"""
    try:
        workspace_url, scope = await validate_databricks_config(db)
        secrets = await get_databricks_secrets(db, scope)
        if secrets is None:
            return []
        return secrets
    except Exception as e:
        logger.error(f"Error getting secrets: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting secrets: {str(e)}")

@router.put("/secrets/{key}")
async def set_secret(key: str, value: str, db: AsyncSession = Depends(get_async_db)):
    """Set a secret value in Databricks"""
    try:
        workspace_url, scope = await validate_databricks_config(db)
        return await set_secret_value(db, scope, key, value)
    except Exception as e:
        logger.error(f"Error setting secret: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error setting secret: {str(e)}")

@router.delete("/secrets/{key}")
async def delete_secret_endpoint(key: str, db: AsyncSession = Depends(get_async_db)):
    """Delete a secret from Databricks"""
    try:
        workspace_url, scope = await validate_databricks_config(db)
        return await delete_secret(db, scope, key)
    except Exception as e:
        logger.error(f"Error deleting secret: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting secret: {str(e)}") 