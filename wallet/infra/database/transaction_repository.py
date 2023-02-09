from sqlite3 import Connection, Cursor
from typing import Any

from wallet.core.transaction.transaction import ITransaction, Transaction
from wallet.core.transaction.transaction_interactor import TransactionRepository


class TransactionRepositoryDb(TransactionRepository):
    def __init__(self, cursor: Cursor, connection: Connection) -> None:
        self.cursor = cursor
        self.connection = connection
        self._create_transactions_table_()

    def _create_transactions_table_(self) -> None:
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS transactions (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               wallet_from INTEGER NOT NULL,
               wallet_to INTEGER NOT NULL,
               amount NUMBER NOT NULL,
               FOREIGN KEY (wallet_from) REFERENCES wallets(id),
               FOREIGN KEY (wallet_to) REFERENCES wallets(id));"""
        )

    def create_transaction(
        self, wallet_from: str, wallet_to: str, amount: float
    ) -> Any:
        self.cursor.execute(
            "INSERT INTO transactions (wallet_from, wallet_to, amount) VALUES (?,?,?)",
            (
                wallet_from,
                wallet_to,
                amount,
            ),
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def fetch_transactions(self, wallet_address: str) -> list[ITransaction]:
        transactions: list[ITransaction] = []
        for (id, wallet_from, wallet_to, amount) in self.cursor.execute(
            "SELECT * from transactions WHERE wallet_from = ? OR wallet_to = ?",
            (wallet_address, wallet_address),
        ):
            transactions.append(Transaction(id, wallet_from, wallet_to, amount))
        return transactions
