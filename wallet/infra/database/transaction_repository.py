from sqlite3 import Cursor, Connection, connect


class TransactionRepository:

    def __init__(self, database_name: str) -> None:
        self.db_name = database_name
        con: Connection = connect(self.db_name)
        cursor: Cursor = con.cursor()
        self.create_transactions_table(cursor)
        con.commit()
        con.close()

    def create_transactions_table(self, cursor: Cursor):
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS transactions (
               id INTEGER PRIMARY KEY,
               wallet_from INTEGER NOT NULL,
               wallet_to INTEGER NOT NULL,
               amount NUMBER NOT NULL,
               FOREIGN KEY (wallet_from) REFERENCES wallets(id),
               FOREIGN KEY (wallet_to) REFERENCES wallets(id));"""
        )
