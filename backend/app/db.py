from typing import Optional
import os

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv


# Load variables from .env if present
load_dotenv()

MONGO_CONNECTION_STRING = os.getenv(
    "MONGODB_URI", "mongodb://localhost:27017"
)
MONGO_DB_NAME = os.getenv("MONGODB_DB_NAME", "money_tracker")

mongo_client: Optional[AsyncIOMotorClient] = None


async def init_db():
    """
    Initialize MongoDB client and Beanie ODM.
    """
    global mongo_client
    if mongo_client is None:
        mongo_client = AsyncIOMotorClient(MONGO_CONNECTION_STRING)

    db = mongo_client[MONGO_DB_NAME]

    # Local import to avoid circular dependencies when models import db
    from app.model.transaction_model import Transaction
    from app.model.category_model import Category

    await init_beanie(database=db, document_models=[Transaction, Category])


async def close_db():
    """
    Close MongoDB client on application shutdown.
    """
    global mongo_client
    if mongo_client is not None:
        mongo_client.close()
        mongo_client = None
