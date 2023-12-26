from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.spread import Spread


class SpreadAlertIn(BaseModel):
    market_id: str = Field(None, min_length=7, max_length=7)
    threshold: float = Field(..., gt=0, le=100)

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "market_id": "BTC-USD",
                    "threshold": 0.1
                }
            ]
        })


class SpreadAlertUpdate(BaseModel):
    market_id: Optional[str] = Field(None, min_length=7, max_length=7)
    threshold: Optional[float] = Field(None, gt=0, le=100)

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "threshold": 0.1
                },
                {
                    "market_id": "BTC-USD"
                },
                {
                    "market_id": "BTC-USD",
                    "threshold": 0.1
                }
            ]
        })


class SpreadAlertOut(SpreadAlertIn):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "market_id": "BTC-USD",
                    "threshold": 0.1,
                    "created_at": "2021-09-24T23:00:00",
                    "updated_at": "2021-09-25T23:00:00"
                }
            ]
        })


class CheckAlertOut(BaseModel):
    triggered: bool = False
    alert: SpreadAlertOut
    spread: Spread

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "triggered": False,
                    "alert": {
                        "id": 1,
                        "market_id": "BTC-USD",
                        "threshold": 0.1,
                        "created_at": "2021-09-22T23:00:00",
                        "updated_at": "2021-09-23T23:00:00"
                    },
                    "spread": {
                        "market_id": "BTC-USD",
                        "base_currency": "BTC",
                        "quote_currency": "USD",
                        "value": 0.1,
                        "threshold": 0.1
                    }
                },
                {
                    "triggered": True,
                    "alert": {
                        "id": 1,
                        "market_id": "BTC-USD",
                        "threshold": 0.1,
                        "created_at": "2021-09-21T23:00:00",
                        "updated_at": "2021-09-21T23:00:00"
                    },
                    "spread": {
                        "market_id": "BTC-USD",
                        "base_currency": "BTC",
                        "quote_currency": "USD",
                        "value": 0.1,
                        "threshold": 0.1
                    }
                }
            ]
        })
