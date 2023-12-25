from pydantic import BaseModel


class Market(BaseModel):
    id: str
    name: str
    base_currency: str
    quote_currency: str
