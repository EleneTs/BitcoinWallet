from dataclasses import field

from wallet.core.statistics.statistics import StatisticsInfo
from wallet.core.statistics.statistics_interactor import StatisticsRepository


class StatisticsRepositoryInMemory(StatisticsRepository):
    statistics: StatisticsInfo = field(default_factory=StatisticsInfo)

    def add_transaction_profit(self, transaction_fee: float):
        self.statistics.platform_profit = (
            self.statistics.platform_profit + transaction_fee
        )
        self.statistics.transactions_count = self.statistics.transactions_count + 1

    def get_statistics(self) -> StatisticsInfo:
        return self.statistics
