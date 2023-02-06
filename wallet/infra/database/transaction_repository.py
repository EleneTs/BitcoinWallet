from sqlite3 import Connection, Cursor


class TransactionRepository:
    def __init__(self, cursor: Cursor, connection: Connection) -> None:
        self.cursor = cursor
        self.connection = connection
        self.create_transactions_table()

    def create_transactions_table(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS transactions (
               id INTEGER PRIMARY KEY,
               wallet_from INTEGER NOT NULL,
               wallet_to INTEGER NOT NULL,
               amount NUMBER NOT NULL,
               FOREIGN KEY (wallet_from) REFERENCES wallets(id),
               FOREIGN KEY (wallet_to) REFERENCES wallets(id));"""
        )
