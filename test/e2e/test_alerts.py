from test.e2e import buda_api_mock, client

from app.schemas.order_book import OrderBook, Record

endpoint_base = '/api/alerts'


def test_add_alert():
    alert_data = {
        "market_id": "BTC-CLP",
        "threshold": 0.1,
    }
    response = client.post(endpoint_base, json=alert_data)
    assert response.status_code == 200
    assert response.json().get('id')
    assert response.json()["market_id"] == alert_data["market_id"]
    assert response.json()["threshold"] == alert_data["threshold"]


def test_get_alerts():
    response = client.get(endpoint_base)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_alert():
    alert_id = 1
    response = client.get(f"{endpoint_base}/{alert_id}")
    assert response.status_code == 200
    assert response.json()["id"] == alert_id


def test_check_alert_false():
    """Test check alert if it is not triggered"""
    buda_api_mock.get_order_book.return_value = OrderBook(
        market_id='btc-clp',
        asks=[Record(price=100, amount=1)],
        bids=[Record(price=90, amount=1)]
    )
    alert_id = 1
    response = client.get(f"{endpoint_base}/{alert_id}/check")
    assert response.status_code == 200
    assert response.json()["triggered"] is False


def test_check_alert_true():
    """Test check alert if it is triggered"""
    buda_api_mock.get_order_book.return_value = OrderBook(
        market_id='btc-clp',
        asks=[Record(price=100.0, amount=1)],
        bids=[Record(price=99.99999, amount=1)]
    )
    alert_id = 1
    response = client.get(f"{endpoint_base}/{alert_id}/check")
    assert response.status_code == 200
    assert response.json()["triggered"] is True


def test_update_alert():
    alert_id = 1
    updated_alert_data = {
        "market_id": "BTC-CLP",
        "threshold": 50.0,
    }
    response = client.patch(
        f"{endpoint_base}/{alert_id}", json=updated_alert_data)
    assert response.status_code == 200
    assert response.json()["id"] == alert_id
    assert response.json()["market_id"] == updated_alert_data["market_id"]
    assert response.json()["threshold"] == updated_alert_data["threshold"]


def test_delete_alert():
    alert_id = 1
    response = client.delete(f"{endpoint_base}/{alert_id}")
    assert response.status_code == 200
    assert response.json()["id"] == alert_id
