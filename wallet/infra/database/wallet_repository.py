from sqlite3 import Connection, Cursor, connect
from typing import Optional

from wallet.core.user.interactor import User
from wallet.core.wallet.wallet import FetchWalletRequest


class WalletRepository:
    def __init__(self, database_name: str) -> None:
        self.db_name = database_name
        con: Connection = connect(self.db_name)
        cursor: Cursor = con.cursor()
        self.create_wallets_table(cursor)
        con.commit()
        con.close()

    def create_wallets_table(self, cursor: Cursor):
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS wallets (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               address TEXT NOT NULL UNIQUE,
               balance NUMBER NOT NULL,
               api_key TEXT NOT NULL,
               FOREIGN KEY (api_key) REFERENCES users(api_key))"""
        )

    def count_user_wallets(self, user: User) -> int:
        con = connect(self.db_name)
        cursor = con.cursor()
        cursor.execute("SELECT COUNT(*) FROM wallets WHERE api_key=?", user.api_key)
        result = cursor.fetchone()
        con.close()
        return result[0] if result is not None else 0

    def create_wallet(
        self, wallet_address: str, btc_balance: float, user: User
    ) -> Optional[FetchWalletRequest]:
        con = connect(self.db_name)
        cursor = con.cursor()
        print(user.api_key)
        print(btc_balance)
        cursor.execute(
            """
               INSERT INTO wallets (address, balance, api_key)
               VALUES (?,?,?)
           """,
            (wallet_address, btc_balance, user.api_key[0]),
        )
        con.commit()
        con.close()
        return self.fetch_wallet(wallet_address=wallet_address)

    def fetch_wallet(self, wallet_address: str) -> Optional[FetchWalletRequest]:
        con = connect(self.db_name)
        cursor = con.cursor()
        cursor.execute(
            """
                    SELECT * FROM wallets
                    WHERE address = ?
                """,
            (wallet_address,),
        )
        result = cursor.fetchone()
        con.close()
        if result:
            return FetchWalletRequest(balance=result[2], wallet_address=result[1])
        return None
