from dataclasses import dataclass
from typing import List, Optional

from wallet.core.user.user import IUser
from wallet.core.wallet.wallet import FetchWalletRequest
from wallet.core.wallet.wallet_interactor import WalletRepository


@dataclass
class WalletInMemoryRepository(WalletRepository):
    def __init__(self) -> None:
        self.wallets = dict()

    def count_user_wallets(self, user: IUser) -> int:
        return sum(
            [
                1
                for wallet in self.wallets.values()
                if wallet["user_id"] == user.get_user_id()
            ]
        )

    def create_wallet(
        self, wallet_address: str, btc_balance: float, user: IUser
    ) -> Optional[FetchWalletRequest]:
        self.wallets[wallet_address] = {
            "wallet_address": wallet_address,
            "btc_balance": btc_balance,
            "user_id": user.get_user_id(),
        }
        return FetchWalletRequest(balance=btc_balance, wallet_address=wallet_address)

    def fetch_wallet(self, wallet_address: str) -> Optional[FetchWalletRequest]:
        wallet = self.wallets.get(wallet_address)
        if wallet:
            return FetchWalletRequest(
                balance=wallet["btc_balance"], wallet_address=wallet_address
            )
        return None

    def fetch_wallet_owner_id(self, wallet_address: str) -> int:
        wallet = self.wallets.get(wallet_address)
        if wallet:
            return int(wallet["user_id"])
        return -1

    def make_transaction(self, wallet_address: str, amount: float) -> None:
        wallet = self.wallets.get(wallet_address)
        if wallet:
            wallet["btc_balance"] += amount

    def get_user_wallets_address(self, user_id: int) -> List[str]:
        return [
            wallet["wallet_address"]
            for wallet in self.wallets.values()
            if wallet["user_id"] == user_id
        ]
