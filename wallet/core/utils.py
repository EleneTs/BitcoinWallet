import uuid
from typing import Protocol

import requests


class Generator(Protocol):
    def generate_key(self) -> str:
        pass


class KeyGenerator:
    def generate_key(self) -> str:
        return str(uuid.uuid4().hex)


class Convertor(Protocol):
    def get_btc_to_usd(self, btc_amount: float) -> float:
        pass


class CoinApiConvertor(Convertor):
    url: str = "https://rest.coinapi.io/v1/exchangerate/BTC/USD"
    api_key: str = "D26CBBDB-3B7F-45BB-B678-040D62E8C654"

    def get_btc_to_usd(self, btc_amount: float) -> float:
        headers = {"X-CoinAPI-Key": self.api_key}
        response = requests.get(self.url, headers=headers)
        exchange_rate = response.json()["rate"]
        return float(round(exchange_rate * btc_amount, 2))
