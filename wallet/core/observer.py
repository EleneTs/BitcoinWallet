from abc import ABC, abstractmethod

from wallet.core.statistics.statistics_interactor import StatisticsRepository


class StatisticsObserver(ABC):
    @abstractmethod
    def update(
        self, transaction_fee: float, statistics_repository: StatisticsRepository
    ):
        pass


class DefaultStatisticsObserver(StatisticsObserver):
    def update(
        self, transaction_fee: float, statistics_repository: StatisticsRepository
    ):
        statistics_repository.add_transaction_profit(transaction_fee)
