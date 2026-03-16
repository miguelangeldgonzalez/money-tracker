from typing import TypedDict


class BinanceC2COrder(TypedDict):
    orderNumber: str
    advNo: str
    tradeType: str
    asset: str
    fiat: str
    fiatSymbol: str
    amount: str
    totalPrice: str
    unitPrice: str
    orderStatus: str
    createTime: int
    commission: str
    takerCommissionRate: str
    takerCommission: str
    takerAmount: str
    counterPartNickName: str
    payMethodName: str
    additionalKycVerify: int

