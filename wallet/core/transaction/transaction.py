from dataclasses import dataclass, field
from http import HTTPStatus
from typing import Optional, Protocol


class ITransaction(Protocol):
    def get_id(self) -> int:
        pass

    def get_wallet_from(self) -> str:
        pass

    def get_wallet_to(self) -> str:
        pass

    def get_amount(self) -> float:
        pass


@dataclass
class Transaction(ITransaction):
    id: int
    wallet_from: str
    wallet_to: str
    amount: float

    def get_id(self) -> int:
        return self.id

    def get_wallet_from(self) -> str:
        return self.wallet_from

    def get_wallet_to(self) -> str:
        return self.wallet_to

    def get_amount(self) -> float:
        return self.amount


@dataclass
class CreateTransactionRequest:
    api_key: str
    wallet_from: str
    wallet_to: str
    amount: float


@dataclass
class Response:
    message: str = ""
    status_code: int = HTTPStatus.OK


@dataclass
class TransactionInfo:
    commission_fee: float = 0.0
    transaction_id: int = 0


@dataclass
class TransactionResponse(Response):
    transaction_info: Optional[TransactionInfo] = field(
        default_factory=lambda: TransactionInfo()
    )


@dataclass
class TransactionListResponse(Response):
    # TODO one mypy error left here
    transactions_list: Optional[list[ITransaction]] = field(
        default_factory=lambda: Transaction(0, "", "", 0)
    )
