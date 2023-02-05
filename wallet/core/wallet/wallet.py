from dataclasses import dataclass, field
from http import HTTPStatus
from typing import Optional, Protocol


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
class FetchWalletRequest:
    balance: float
    wallet_address: str
