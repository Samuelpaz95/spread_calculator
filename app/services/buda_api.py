import base64
import hmac
import logging
import os
import queue
import threading
import time
import traceback
from typing import Callable

import requests
from fastapi import HTTPException
from requests import PreparedRequest

from app.schemas.market import Market
from app.schemas.order_book import OrderBook


class BudaApi:
    def __init__(self):
        self.key = os.environ.get("BUDA_API_KEY")
        self.secret = os.environ.get("BUDA_API_SECRET")
        self.base_url = os.environ.get("BUDA_API_URL")
        self.req_queue = queue.Queue()

        if not self.key or not self.secret or not self.base_url:
            raise TypeError("Buda API credentials not found")

    def store_request(request_fn: Callable):
        def wrapper(*args, **kwargs):
            args[0].req_queue.put(request_fn(*args, **kwargs))
        return wrapper

    def get_nonce(self):
        return str(int(time.time() * 1e6))

    def sign(self, request: PreparedRequest, nonce: str):
        components = [request.method, request.path_url]
        if request.body:
            encoded_body = base64.b64encode((request.body)).decode()
            components.append(encoded_body)
        components.append(nonce)
        message = " ".join(components)
        h = hmac.new(key=self.secret.encode(),
                     msg=message.encode(), digestmod="sha384")
        return h.hexdigest()

    def __call__(self, request: PreparedRequest):
        nonce = self.get_nonce()
        signature = self.sign(request, nonce)
        request.headers.update({
            "X-SBTC-APIKEY": self.key,
            "X-SBTC-NONCE": nonce,
            "X-SBTC-SIGNATURE": signature
        })
        return request

    def get(self, url: str) -> dict:
        url = os.path.join(self.base_url, url)
        response = requests.get(url, auth=self)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code,
                                detail=response.json())
        return response.json()

    def get_order_book(self, market_id: str) -> OrderBook:
        url = f"markets/{market_id}/order_book"
        order_book = self.get(url).get('order_book')
        order_book['market_id'] = market_id
        return OrderBook.from_dict(order_book)

    @store_request
    def get_async_order_book(self, market_id: str) -> dict | None:
        try:
            return self.get_order_book(market_id)
        except Exception:
            traceback.print_exc()
            return None

    def get_all_order_books(self) -> list[OrderBook | None]:
        markets = self.get("markets").get("markets")

        threads: list[threading.Thread] = []
        for market in markets:
            time.sleep(1 / len(markets))  # avoid rate limit
            thread = threading.Thread(target=self.get_async_order_book,
                                      args=[market.get('id')])
            threads.append(thread)
            thread.start()

        return [self.req_queue.get() for _ in threads]

    def get_markets(self) -> list[Market]:
        markets = self.get("markets").get("markets")
        return [Market(**market) for market in markets]


__all__ = ["BudaApi"]
