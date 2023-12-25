from pydantic import BaseModel, Field


class Book(BaseModel):
    price: float = Field(..., alias="price")
    amount: float = Field(..., alias="amount")


class OrderBook(BaseModel):
    market_id: str = Field(..., alias="market_id")
    asks: list[Book] = Field(..., alias="asks")
    bids: list[Book] = Field(..., alias="bids")

    @classmethod
    def from_dict(cls, data: dict) -> "OrderBook":
        asks = [Book(price=float(price), amount=float(amount))
                for price, amount in data.pop('asks')]
        bids = [Book(price=float(price), amount=float(amount))
                for price, amount in data.pop('bids')]
        return cls(**data, asks=asks, bids=bids)
