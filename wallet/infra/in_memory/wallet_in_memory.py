from dataclasses import dataclass
from typing import Dict, List, Optional, Union

from wallet.core.user.user import IUser
from wallet.core.wallet.wallet import FetchWalletRequest
from wallet.core.wallet.wallet_interactor import WalletRepository


@dataclass
class WalletInMemoryRepository(WalletRepository):
    def __init__(self) -> None:
        self.wallets: Dict[str, Dict[str, Union[str, float, int]]] = {}

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
        fetched_wallet = self.wallets.get(wallet_address)
        assert fetched_wallet is not None
        balance = fetched_wallet["btc_balance"]
        if fetched_wallet:
            return FetchWalletRequest(
                balance=float(balance), wallet_address=wallet_address
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
            wallet["btc_balance"] = float(wallet["btc_balance"]) + amount

    def get_user_wallets_address(self, user_id: int) -> List[str]:
        return [
            str(wallet["wallet_address"])
            for wallet in self.wallets.values()
            if wallet["user_id"] == user_id
        ]
