from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional
from beanie import Document, Link
from app.model.category_model import Category

class Transaction(Document):
    amount: float
    unitPrice: float
    fiat: str
    description: Optional[str] = None
    orderCreatedAt: datetime
    createdAt: datetime = datetime.now()
    category: Link[Category]

    class Settings:
        name = "transactions"

