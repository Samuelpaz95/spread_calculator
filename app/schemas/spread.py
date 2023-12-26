from pydantic import BaseModel, ConfigDict, Field, field_serializer


class Spread(BaseModel):
    market_id: str = Field(..., alias="market_id")
    value: float = Field(None, alias="value",
                         description="The value of the spread")
    percentage: float = Field(None, alias="percentage",
                              description="The percentage of the spread (0.00% to 100.00%)")
    base_currency: str = Field(..., alias="base_currency")
    quote_currency: str = Field(..., alias="quote_currency")

    model_config = ConfigDict(
        json_schema_extra={
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
        }, json_round_trip=True
    )

    @field_serializer('value')
    def serialize_value(self, value: float, _info) -> float:
        return round(value, 8) if value is not None else None

    @field_serializer('percentage')
    def serialize_percentage(self, percentage: float, _info) -> float:
        return round(percentage, 2) if percentage is not None else None
