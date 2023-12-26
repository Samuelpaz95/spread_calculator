from fastapi import APIRouter, Depends

from app.schemas.spread_alert import (CheckAlertOut, SpreadAlertIn,
                                      SpreadAlertOut, SpreadAlertUpdate)
from app.services.alert_service import AlertService

alerts_router = APIRouter(prefix='/alerts', tags=['Alerts'])


@alerts_router.post("/")
async def add_alert(spread_alert_in: SpreadAlertIn, service: AlertService = Depends()) -> SpreadAlertOut:
    """Add an alert.

    ### Request Body:
    - **SpreadAlertIn**: The alert to add.
        - **market_id**: The market id.
        - **threshold**: The spread threshold value to trigger the alert.

    ### Response:
    - **SpreadAlertOut**: The added alert.

    """
    return service.add_alert(spread_alert_in)


@alerts_router.get("/")
async def get_alerts(service: AlertService = Depends()) -> list[SpreadAlertOut]:
    """Get all alerts.

    ### Response:
    - **List[SpreadAlertOut]**: A list of spread alerts.

    """
    return service.get_alerts()


@alerts_router.get("/{alert_id}")
async def get_alert(alert_id: int, service: AlertService = Depends()) -> SpreadAlertOut:
    """Get an alert by id.

    ### Response:
    - **SpreadAlertOut**: The spread alert.

    """
    return service.get_alert(alert_id)


@alerts_router.get("/{alert_id}/check")
async def check_alert(alert_id: int, service: AlertService = Depends()) -> CheckAlertOut:
    """Check if an alert has been triggered.

    ### Response:
    - **Dict[alert: SpreadAlertOut | None]**: The alert if it has been triggered.
    """
    return service.check_alerts(alert_id)


@alerts_router.patch("/{alert_id}")
async def update_alert(alert_id: int, spread_alert_data: SpreadAlertUpdate, service: AlertService = Depends()) -> SpreadAlertOut:
    """Update an alert.

    ### Request Body:
    - **SpreadAlertUpdate**: The alert data to update.
        - **market_id** (optional): The market id.
        - **threshold** (optional): The spread threshold value to trigger the alert.

    ### Response:
    - **SpreadAlertOut**: The updated alert.

    """
    return service.update_alert(alert_id, spread_alert_data)


@alerts_router.delete("/{alert_id}")
async def delete_alert(alert_id: int, service: AlertService = Depends()) -> SpreadAlertOut:
    """Delete an alert.

    ### Response:
    - **SpreadAlertOut**: The deleted alert.

    """
    return service.delete_alert(alert_id)
