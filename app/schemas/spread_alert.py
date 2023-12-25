from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.spread import Spread


class SpreadAlertIn(BaseModel):
    market_id: str = Field(None, min_length=7, max_length=7)
    percentage: float = Field(..., gt=0, le=100)

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "market_id": "BTC-USD",
                    "percentage": 0.1
                }
            ]
        }


class SpreadAlertUpdate(BaseModel):
    market_id: Optional[str] = Field(None, min_length=7, max_length=7)
    percentage: Optional[float] = Field(None, gt=0, le=100)

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "percentage": 0.1
                },
                {
                    "market_id": "BTC-USD"
                },
                {
                    "market_id": "BTC-USD",
                    "percentage": 0.1
                }
            ]
        }


class SpreadAlertOut(SpreadAlertIn):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "id": 1,
                    "market_id": "BTC-USD",
                    "percentage": 0.1,
                    "created_at": "2021-09-23T23:00:00",
                    "updated_at": "2021-09-23T23:00:00"
                }
            ]
        }


class CheckAlertOut(BaseModel):
    alert: SpreadAlertOut | None
    spread: Spread | None

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "alert": {
                        "id": 1,
                        "market_id": "BTC-USD",
                        "percentage": 0.1,
                        "created_at": "2021-09-21T23:00:00",
                        "updated_at": "2021-09-21T23:00:00"
                    },
                    "spread": {
                        "market_id": "BTC-USD",
                        "base_currency": "BTC",
                        "quote_currency": "USD",
                        "value": 0.1,
                        "percentage": 0.1
                    }
                },
                {
                    "alert": None,
                    "spread": None
                }
            ]
        }
