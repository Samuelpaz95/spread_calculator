from http.client import BAD_REQUEST, NOT_FOUND

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import get_db
from app.models.spread_alert import SpreadAlert
from app.schemas.order_book import OrderBook
from app.schemas.spread import Spread
from app.schemas.spread_alert import (CheckAlertOut, SpreadAlertIn,
                                      SpreadAlertOut, SpreadAlertUpdate)
from app.services.buda_api import BudaApi


class SpreadService:
    def __init__(self, buda_api: BudaApi = Depends(), db: Session = Depends(get_db)):
        self.buda_api = buda_api
        self.db = db

    def get_spreads(self) -> list[Spread]:
        order_books = self.buda_api.get_all_order_books()
        order_books = [order_book for order_book in order_books if
                       order_book is not None]
        return [self.get_spread(order_book) for order_book in order_books]

    def get_market_spread(self, market_id: str) -> Spread:
        order_book = self.buda_api.get_order_book(market_id)
        return self.get_spread(order_book)

    def get_spread(self, order_book: OrderBook) -> Spread:
        base_currency, quote_currency = order_book.market_id.split('-')

        spread = Spread(
            market_id=order_book.market_id,
            base_currency=base_currency,
            quote_currency=quote_currency)

        if not order_book.asks or not order_book.bids:
            return spread

        min_ask = order_book.asks[0].price  # the first ask is the lowest
        max_bid = order_book.bids[0].price  # the first bid is the highest
        spread.value = min_ask - max_bid
        spread.percentage = spread.value / max_bid * 100
        return spread
