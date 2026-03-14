from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from sqlalchemy.orm import Session

from app import db as db_module


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_module.mongo_client = AsyncIOMotorClient(db_module.MONGO_CONNECTION_STRING)
    try:
        yield
    finally:
        if db_module.mongo_client is not None:
            db_module.mongo_client.close()


app = FastAPI(title="Money Tracker Backend", lifespan=lifespan)


@app.get("/health")
async def health_check(
    sql_db: Session = Depends(db_module.get_db),
    mongo_db: AsyncIOMotorDatabase = Depends(db_module.get_mongo_db),
):
    sql_db.execute("SELECT 1")
    await mongo_db.command("ping")
    return {"status": "ok"}


@app.get("/")
async def root():
    return {"message": "Money Tracker Backend is running"}

