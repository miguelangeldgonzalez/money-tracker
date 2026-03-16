
from fastapi import APIRouter, HTTPException, Depends
from app.dependencies import verify_auth0_token
from app.transaction.transaction_service import fetch_last_transaction_history, create_transaction
from pydantic import BaseModel

router = APIRouter(
    prefix="/transaction",
    tags=["transaction"],
    dependencies=[Depends(verify_auth0_token)]
)


@router.get("/get_last_transaction")
async def register_last_transaction():
    try: 
        data = await fetch_last_transaction_history()
        return data
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# Pydantic model for transaction creation
class TransactionCreateRequest(BaseModel):
    amount: float
    unitPrice: float
    fiat: str
    description: str | None = None
    orderCreatedAt: str  # ISO format string
    category_id: str

@router.post("/create")
async def create_new_transaction(payload: TransactionCreateRequest):
    try:
        transaction = await create_transaction(payload)
        return transaction
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))