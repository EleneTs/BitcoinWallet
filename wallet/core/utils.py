import uuid
from typing import Protocol

import requests


class Generator(Protocol):
    def generate_key(self):
        pass


class KeyGenerator:
    def generate_key(self):
        return str(uuid.uuid4().hex)


class Convertor(Protocol):
    def get_btc_to_usd(self, btc_amount: float) -> float:
        pass


class CoinApiConvertor(Convertor):
    url: str = "https://rest.coinapi.io/v1/exchangerate/BTC/USD"
    api_key: str = "D03D9113-20F7-4E49-9A40-D86314C02B8F" # over the limit of 100 requests

    def get_btc_to_usd(self, btc_amount: float) -> float:
        headers = {"X-CoinAPI-Key": self.api_key}
        response = requests.get(self.url, headers=headers)
        exchange_rate = response.json()["rate"]
        return round(exchange_rate * btc_amount, 2)
