from app.model.transaction_model import Transaction
from app.model.category_model import Category
from beanie import PydanticObjectId
from dotenv import load_dotenv
from datetime import datetime
import os
import hmac
import hashlib
import httpx

from app.types.transaction import BinanceC2COrder


load_dotenv()

BINANCE_BASE_URL = "https://api.binance.com"
API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

async def create_transaction(payload):
    # Find the category by ID
    category = await Category.get(PydanticObjectId(payload.category_id))
    if not category:
        raise ValueError("Category not found")
    # Parse orderCreatedAt
    order_created_at = datetime.fromisoformat(payload.orderCreatedAt)
    transaction = Transaction(
        amount=payload.amount,
        unitPrice=payload.unitPrice,
        fiat=payload.fiat,
        description=payload.description,
        orderCreatedAt=order_created_at,
        category=category
    )
    await transaction.insert()
    return transaction


async def fetch_last_transaction_history() -> BinanceC2COrder:
    """
    Equivalent behavior to get-history.sh:
    - Get server time from Binance
    - Build signed query with recvWindow and timestamp
    - Call the C2C user order history endpoint
    """
    if not API_KEY or not SECRET_KEY:
        raise RuntimeError("API_KEY or SECRET_KEY not configured in environment")

    async with httpx.AsyncClient() as client:
        # 1. Get server time
        time_resp = await client.get(f"{BINANCE_BASE_URL}/api/v3/time")
        time_resp.raise_for_status()
        server_time = time_resp.json().get("serverTime")

        if server_time is None:
            raise RuntimeError("Could not obtain serverTime from Binance")

        # 2. Build query: request only the most recent order (page=1, rows=1)
        # According to Binance docs for GET /sapi/v1/c2c/orderMatch/listUserOrderHistory,
        # results are paginated and ordered by time desc by default, so page=1&rows=1
        # gives us the latest user order.
        query = f"recvWindow=60000&timestamp={server_time}&page=1&rows=1"

        # 3. Sign with HMAC SHA256
        signature = hmac.new(
            SECRET_KEY.encode("utf-8"),
            query.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        # 4. Perform the request
        headers = {"X-MBX-APIKEY": API_KEY}
        url = (
            f"{BINANCE_BASE_URL}/sapi/v1/c2c/orderMatch/listUserOrderHistory"
            f"?{query}&signature={signature}"
        )

        resp = await client.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()["data"][0]

