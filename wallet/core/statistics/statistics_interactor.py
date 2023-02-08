from dataclasses import dataclass
from http import HTTPStatus
from typing import Protocol

from wallet.core.statistics.statistics import (StatisticsInfo,
                                               StatisticsResponse)

ADMIN_API_KEY = "1d95d3aa5dcd48189edc62582cc9c288"


class StatisticsRepository(Protocol):
    def add_transaction_profit(self, transaction_fee: float):
        pass

    def get_statistics(self) -> StatisticsInfo:
        pass


@dataclass
class StatisticsInteractor:
    statistics_repository: StatisticsRepository

    def add_transaction_profit(self, transaction_fee: float):
        self.statistics_repository.add_transaction_profit(transaction_fee)

    def get_statistics(self, admin_api_key: str) -> StatisticsResponse:
        if admin_api_key == ADMIN_API_KEY:
            statistics = self.statistics_repository.get_statistics()
            return StatisticsResponse(
                status_code=HTTPStatus.OK, statistics_info=statistics
            )
        return StatisticsResponse(
            status_code=HTTPStatus.FORBIDDEN, message="Admin Api Key not correct"
        )
