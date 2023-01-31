from sqlite3 import Connection, connect, Cursor


class WalletRepository:

    def __init__(self, database_name: str) -> None:
        self.db_name = database_name
        con: Connection = connect(self.db_name)
        cursor: Cursor = con.cursor()
        self.create_tables(cursor)
        con.commit()
        con.close()

    def create_tables(self, cursor: Cursor):
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS wallets (
               id INTEGER PRIMARY KEY,
               address TEXT NOT NULL UNIQUE,
               balance NUMBER NOT NULL)"""
        )

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users_wallets (
               id INTEGER PRIMARY KEY,
               user_id INTEGER NOT NULL,
               wallet_id INTEGER NOT NULL,
               FOREIGN KEY (user_id) REFERENCES users(id),
               FOREIGN KEY (wallet_id) REFERENCES wallets(id));"""
        )
