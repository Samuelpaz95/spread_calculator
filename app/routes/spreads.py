from fastapi import APIRouter, Depends

from app.schemas.spread import Spread
from app.services.spread_service import SpreadService

spreads_router = APIRouter(prefix='/spreads', tags=['Spreads'])


@spreads_router.get('/')
async def bread(service: SpreadService = Depends()) -> list[Spread]:
    """This function returns a list of spreads.

    ### Returns:
    - **List[Spread]**: A list of spreads.
    """
    return service.get_spreads()


@spreads_router.get('/{market_id}')
async def spread_by_market(market_id: str, service: SpreadService = Depends()) -> Spread:
    """Get the spread for a specific market.

    ### Parameters:
    - **market_id**: The market id.

    ### Response:
    - **Spread**: The spread for the market.

    """
    return service.get_market_spread(market_id)
