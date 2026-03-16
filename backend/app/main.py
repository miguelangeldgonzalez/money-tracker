from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.dependencies import verify_auth0_token

from app import db as db_module
from app.model.transaction_model import Transaction

from app.transaction.transaction_controller import router as transaction_router
from app.category_controller import router as category_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_module.init_db()
    try:
        yield
    finally:
        await db_module.close_db()




app = FastAPI(title="Money Tracker Backend", lifespan=lifespan)

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],  # Add your frontend URLs here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(transaction_router)
app.include_router(category_router)

def secure_dependency(dep=Depends(verify_auth0_token)):
    pass


@app.get("/health", dependencies=[Depends(verify_auth0_token)])
async def health_check():
    # Simple Beanie query to verify MongoDB connectivity
    _ = await Transaction.find().limit(1).to_list()
    return {"status": "ok"}


@app.get("/", dependencies=[Depends(verify_auth0_token)])
async def root():
    return {"message": "Money Tracker Backend with Beanie is running"}

