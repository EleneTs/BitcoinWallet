from typing import Protocol

import requests


class Convertor(Protocol):
    def get_btc_to_usd(self, btc_amount: float) -> float:
        pass


class CoinApiConvertor(Convertor):
    url: str = 'https://rest.coinapi.io/v1/exchangerate/BTC/USD'
    api_key: str = '95E4F109-1AEF-47A0-95AB-26A45AF590D9'

    def get_btc_to_usd(self, btc_amount: float) -> float:
        headers = {'X-CoinAPI-Key': self.api_key}
        response = requests.get(self.url, headers=headers)
        exchange_rate = response.json()['rate']
        return round(exchange_rate * btc_amount, 2)
