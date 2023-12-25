from pydantic import BaseModel, Field


class Spread(BaseModel):
    market_id: str = Field(..., alias="market_id")
    value: float = Field(None, alias="value")
    percentage: float = Field(None, alias="percentage")
    base_currency: str = Field(..., alias="base_currency")
    quote_currency: str = Field(..., alias="quote_currency")

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "market_id": "BTC-USD",
                    "value": 12342,
                    "percentage": 0.12,
                    "base_currency": "BTC",
                    "quote_currency": "USD",
                },
                {
                    "market_id": "ETH-CLP",
                    "value": 12342.00,
                    "percentage": 0.12,
                    "base_currency": "ETH",
                    "quote_currency": "CLP",

                }
            ]
        }
        json_round_trip = True
        json_encoders = {
            float: lambda v: round(v, 8) if v is not None else None,
        }
