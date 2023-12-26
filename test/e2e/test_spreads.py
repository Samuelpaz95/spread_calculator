import math
from test.e2e import buda_api_mock, client

from app.schemas.order_book import OrderBook, Record


def test_get_spreads():
    response = client.get('/api/spreads/')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_spread_by_market():
    buda_api_mock.get_order_book.return_value = OrderBook(
        market_id='btc-clp',
        asks=[Record(price=100, amount=1)],
        bids=[Record(price=90, amount=1)]
    )
    response = client.get('/api/spreads/btc-clp')
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()['market_id'] == 'btc-clp'
    assert response.json()['base_currency'] == 'btc'
    assert response.json()['quote_currency'] == 'clp'
    assert response.json()['value'] == 10
    assert math.isclose(response.json()['percentage'], 11.11, rel_tol=1e-2)
