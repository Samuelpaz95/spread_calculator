from unittest.mock import Mock

from app.schemas.order_book import OrderBook, Record
from app.services.buda_api import BudaApi


class BudaApiMock(Mock(spec=BudaApi)):
    def __init__(self):
        self.get_order_book = Mock()
        self.get_all_order_books = Mock()


buda_api_mock = BudaApiMock()

buda_api_mock.get_all_order_books.return_value = [
    OrderBook(
        market_id='btc-clp',
        asks=[Record(price=100, amount=1)],
        bids=[Record(price=90, amount=1)]
    ),
    OrderBook(
        market_id='eth-clp',
        asks=[Record(price=100, amount=1)],
        bids=[Record(price=90, amount=1)]
    )
]

buda_api_mock.get_order_book.return_value = OrderBook(
    market_id='btc-clp',
    asks=[Record(price=100, amount=1)],
    bids=[Record(price=90, amount=1)]
)
