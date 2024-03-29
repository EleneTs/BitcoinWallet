from sqlite3 import Connection, Cursor
from typing import Any, Optional

from wallet.core.user.user import IUser
from wallet.core.wallet.wallet import FetchWalletRequest
from wallet.core.wallet.wallet_interactor import WalletRepository


class WalletRepositoryDb(WalletRepository):
    def __init__(self, cursor: Cursor, connection: Connection) -> None:
        self.cursor = cursor
        self.connection = connection
        self._create_wallets_table_()

    def _create_wallets_table_(self) -> None:
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS wallets (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               address TEXT NOT NULL UNIQUE,
               balance NUMBER NOT NULL,
               user_id TEXT NOT NULL,
               FOREIGN KEY (user_id) REFERENCES users(id))"""
        )

    def count_user_wallets(self, user: IUser) -> Any:
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

    def fetch_wallet_owner_id(self, wallet_address: str) -> int:
        self.cursor.execute(
            """
                    SELECT * FROM wallets
                    WHERE address = ?
                """,
            (wallet_address,),
        )
        result = self.cursor.fetchone()
        if result:
            return int(result[3])
        return -1

    def make_transaction(self, wallet_address: str, amount: float) -> None:
        wallet = self.fetch_wallet(wallet_address)
        if wallet is not None:
            current_balance = wallet.balance
            new_balance = round(current_balance + amount, 5)
            self.cursor.execute(
                "UPDATE wallets SET balance = ? WHERE address = ? ",
                (new_balance, wallet_address),
            )
            self.connection.commit()

    def get_user_wallets_address(self, user_id: int) -> list[str]:
        user_wallets: list[str] = []
        for (id, address, balance, user_id) in self.cursor.execute(
            "SELECT * from wallets WHERE user_id = ?", (user_id,)
        ):
            user_wallets.append(address)
        return user_wallets
