from dataclasses import dataclass, field
from http import HTTPStatus
from typing import Optional, Protocol

from wallet.core.user.user import IUser, User


class IWallet(Protocol):
    def get_user_id(self) -> int:
        pass

    def get_btc_balance(self) -> str:
        pass

    def get_usd_balance(self) -> str:
        pass

    def get_wallet_address(self) -> float:
        pass


@dataclass
class Wallet(IWallet):
    wallet_address: str = ""
    btc_balance: float = 0.0
    usd_balance: float = 0.0
    user_id: int = 0

    def get_user_id(self) -> int:
        return self.user_id

    def get_btc_balance(self) -> str:
        return self.get_btc_balance()

    def get_usd_balance(self) -> str:
        return self.get_usd_balance()

    def get_wallet_address(self) -> float:
        return self.get_wallet_address()


@dataclass
class Response:
    message: str = ""
    status_code: int = HTTPStatus.OK


@dataclass
class WalletInfo:
    wallet_address: str = ""
    btc_balance: float = 0.0
    usd_balance: float = 0.0


@dataclass
class WalletResponse(Response):
    wallet_info: Optional[WalletInfo] = field(default_factory=lambda: WalletInfo())


@dataclass
class WalletOwnerResponse(Response):
    wallet_owner: Optional[IUser] = field(default_factory=lambda: User(-1, "", ""))


@dataclass
class FetchWalletRequest:
    balance: float
    wallet_address: str
