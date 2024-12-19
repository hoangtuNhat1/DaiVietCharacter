from redis import asyncio as redis
from src.config import Config

JTI_EXPIRY = 3600

# Initialize Redis connection
token_blocklist = redis.Redis(
    host=Config.REDIS_HOST, 
    port=Config.REDIS_PORT, 
    db=0,
    decode_responses=True  # This ensures responses are decoded to strings
)


async def add_jti_to_blocklist(jti: str) -> None:
    """
    Add a JWT token ID to the blocklist with an expiration time.
    
    Args:
        jti (str): The JWT token ID to blocklist
    """
    await token_blocklist.set(name=jti, value="1", ex=JTI_EXPIRY)


async def token_in_blocklist(jti: str) -> bool:
    """
    Check if a JWT token ID is in the blocklist.
    
    Args:
        jti (str): The JWT token ID to check
        
    Returns:
        bool: True if token is blocklisted, False otherwise
    """
    exists = await token_blocklist.exists(jti)
    return bool(exists)