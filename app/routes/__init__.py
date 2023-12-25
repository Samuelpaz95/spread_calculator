from fastapi import APIRouter

from .alerts import alerts_router
from .spreads import spreads_router

router = APIRouter(prefix="/api")
router.include_router(spreads_router)
router.include_router(alerts_router)

__all__ = ["router"]
