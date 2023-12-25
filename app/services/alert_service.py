from http.client import BAD_REQUEST, NOT_FOUND

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import get_db
from app.models.spread_alert import SpreadAlert
from app.schemas.spread_alert import (CheckAlertOut, SpreadAlertIn,
                                      SpreadAlertOut, SpreadAlertUpdate)
from app.services.spread_service import SpreadService


class AlertService:
    def __init__(self, spread_service: SpreadService = Depends(),
                 db: Session = Depends(get_db)) -> None:
        self.spread_service = spread_service
        self.db = db

    def add_alert(self, spread_alert_in: SpreadAlertIn) -> SpreadAlertOut:
        spread = self.spread_service.get_market_spread(
            spread_alert_in.market_id)
        if spread_alert_in.percentage >= spread.percentage:
            raise HTTPException(status_code=BAD_REQUEST,
                                detail="The alert percentage must be lower than the current spread percentage")
        new_alert = SpreadAlert(**spread_alert_in.dict())
        self.db.add(new_alert)
        self.db.commit()
        self.db.refresh(new_alert)
        return new_alert

    def update_alert(self, alert_id, spread_alert_data: SpreadAlertUpdate) -> SpreadAlertOut:
        alert = self.get_alert(alert_id)
        for field, value in spread_alert_data.dict(exclude_unset=True).items():
            setattr(alert, field, value)
        self.db.add(alert)
        self.db.commit()
        return alert

    def get_alerts(self) -> list[SpreadAlertOut]:
        return self.db.query(SpreadAlert).all()

    def get_alert(self, alert_id: int) -> SpreadAlertOut:
        alert = self.db.query(SpreadAlert).filter(
            SpreadAlert.id == alert_id).first()
        if not alert:
            raise HTTPException(status_code=NOT_FOUND,
                                detail="Alert not found")
        return alert

    def delete_alert(self, market_id: str) -> SpreadAlertOut:
        alert = self.get_alert(market_id)
        self.db.delete(alert)
        self.db.commit()
        return alert

    def check_alerts(self, alert_id: int) -> CheckAlertOut:
        alert = self.get_alert(alert_id)
        spread = self.spread_service.get_market_spread(alert.market_id)
        print(alert.percentage, spread.percentage)
        if alert.percentage >= spread.percentage:
            return CheckAlertOut(alert=alert, spread=spread)
        return CheckAlertOut(alert=None, spread=None)
