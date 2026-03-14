from typing import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

MONGO_CONNECTION_STRING = "mongodb://localhost:27017"
MONGO_DB_NAME = "money_tracker"

mongo_client: AsyncIOMotorClient | None = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_mongo_db() -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    if mongo_client is None:
        raise RuntimeError("Mongo client is not initialized")
    db = mongo_client[MONGO_DB_NAME]
    yield db
