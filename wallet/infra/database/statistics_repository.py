from sqlite3 import Connection, Cursor

from wallet.core.statistics.statistics import StatisticsInfo
from wallet.core.statistics.statistics_interactor import StatisticsRepository


class StatisticsRepositoryDB(StatisticsRepository):
    def __init__(self, cursor: Cursor, connection: Connection) -> None:
        self.cursor = cursor
        self.connection = connection
        self.__create_statistics_table__()

    def __create_statistics_table__(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS statistics (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            profit NUMBER,
            transactions_count INTEGER);"""
        )
        self.cursor.execute(
            "INSERT INTO statistics (profit, transactions_count) VALUES (?,?)",
            (
                0,
                0,
            ),
        )
        self.connection.commit()

    def add_transaction_profit(self, transaction_fee: float):
        self.cursor.execute("SELECT * from statistics WHERE id = ?", (1,))
        statistics = self.cursor.fetchone()
        current_profit = statistics[1]
        current_count = statistics[2]
        updated_profit = current_profit + transaction_fee
        updated_count = current_count + 1
        self.cursor.execute(
            "UPDATE statistics SET profit = ?, transactions_count = ? WHERE id = ? ",
            (updated_profit, updated_count, 1),
        )
        self.connection.commit()

    def get_statistics(self) -> StatisticsInfo:
        self.cursor.execute("SELECT * from statistics WHERE id = ?", (1,))
        statistics = self.cursor.fetchone()
        return StatisticsInfo(
            platform_profit=statistics[1], transactions_count=statistics[2]
        )
