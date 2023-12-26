from pydantic import BaseModel, Field


class Record(BaseModel):
    price: float = Field(..., alias="price")
    amount: float = Field(..., alias="amount")


class OrderBook(BaseModel):
    market_id: str = Field(..., alias="market_id")
    asks: list[Record] = Field(..., alias="asks")
    bids: list[Record] = Field(..., alias="bids")

    @classmethod
    def from_dict(cls, data: dict) -> "OrderBook":
        if 'asks' not in data or 'bids' not in data:
            raise ValueError('Invalid order book data')
        asks = [Record(price=float(price), amount=float(amount))
                for price, amount in data.pop('asks')]
        bids = [Record(price=float(price), amount=float(amount))
                for price, amount in data.pop('bids')]
        return cls(**data, asks=asks, bids=bids)
