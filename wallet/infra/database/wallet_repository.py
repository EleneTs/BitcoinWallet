from sqlite3 import Connection, Cursor
from typing import Optional

from wallet.core.user.user_interactor import IUser
from wallet.core.wallet.wallet import FetchWalletRequest


class WalletRepository:
    def __init__(self, cursor: Cursor, connection: Connection) -> None:
        self.cursor = cursor
        self.connection = connection
        self.create_wallets_table()

    def create_wallets_table(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS wallets (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               address TEXT NOT NULL UNIQUE,
               balance NUMBER NOT NULL,
               user_id TEXT NOT NULL,
               FOREIGN KEY (user_id) REFERENCES users(id))"""
        )

    def count_user_wallets(self, user: IUser) -> int:
        self.cursor.execute(
            "SELECT COUNT(*) FROM wallets WHERE user_id=?", (user.get_user_id(),)
        )
        result = self.cursor.fetchone()
        return result[0] if result is not None else 0

    def create_wallet(
        self, wallet_address: str, btc_balance: float, user: IUser
    ) -> Optional[FetchWalletRequest]:

        self.cursor.execute(
            """
               INSERT INTO wallets (address, balance, user_id)
               VALUES (?,?,?)
           """,
            (wallet_address, btc_balance, user.get_user_id()),
        )
        self.connection.commit()
        return self.fetch_wallet(wallet_address=wallet_address)

    def fetch_wallet(self, wallet_address: str) -> Optional[FetchWalletRequest]:
        self.cursor.execute(
            """
                    SELECT * FROM wallets
                    WHERE address = ?
                """,
            (wallet_address,),
        )
        result = self.cursor.fetchone()
        if result:
            return FetchWalletRequest(balance=result[2], wallet_address=result[1])
        return None
