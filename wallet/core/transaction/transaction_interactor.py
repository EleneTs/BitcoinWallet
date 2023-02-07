from dataclasses import dataclass
from http import HTTPStatus
from typing import Protocol

from wallet.core.transaction.transaction import (
    CreateTransactionRequest,
    ITransaction,
    TransactionInfo,
    TransactionListResponse,
    TransactionResponse,
)
from wallet.core.user.user_interactor import UserRepository
from wallet.core.wallet.wallet import WalletOwnerResponse
from wallet.core.wallet.wallet_interactor import WalletRepository

COMMISSION_FEE = 0.015


class TransactionRepository(Protocol):
    def create_transaction(
        self, wallet_from: str, wallet_to: str, amount: float
    ) -> int:
        pass

    def fetch_transactions(self, wallet_address) -> list[ITransaction]:
        pass


@dataclass
class TransactionInteractor:
    user_repository: UserRepository
    wallet_repository: WalletRepository
    transaction_repository: TransactionRepository

    def create_transaction(self, request: CreateTransactionRequest):
        api_user = self.user_repository.fetch_user(request.api_key)
        wallet_from_user = self.__get_wallet_owner__(address=request.wallet_from)
        wallet_to_user = self.__get_wallet_owner__(address=request.wallet_to)
        if (
            wallet_from_user.status_code != HTTPStatus.OK
            or wallet_to_user.status_code != HTTPStatus.OK
            or not api_user
            or api_user.get_user_id() != wallet_from_user.wallet_owner.get_user_id()
        ):
            return TransactionResponse(
                status_code=HTTPStatus.BAD_REQUEST, message="Invalid credentials"
            )
        wallet_request = self.wallet_repository.fetch_wallet(request.wallet_from)
        if wallet_request is not None:
            if request.amount > wallet_request.balance:
                return TransactionResponse(
                    status_code=HTTPStatus.BAD_REQUEST, message="Not enough balance"
                )
        commission_fee: float = 0.0

        if (
            wallet_from_user.wallet_owner.get_user_id()
            == wallet_to_user.wallet_owner.get_user_id()
        ):
            # no commission
            self.wallet_repository.make_transaction(
                request.wallet_from, -request.amount
            )
            self.wallet_repository.make_transaction(request.wallet_to, request.amount)
        else:
            # commission
            # TODO add to statistics
            commission_fee = round(request.amount * COMMISSION_FEE, 5)
            full_amount = round(request.amount + commission_fee, 5)
            self.wallet_repository.make_transaction(request.wallet_from, -full_amount)
            self.wallet_repository.make_transaction(request.wallet_to, request.amount)

        transaction_id = self.transaction_repository.create_transaction(
            request.wallet_from, request.wallet_to, request.amount
        )

        return TransactionResponse(
            status_code=HTTPStatus.CREATED,
            transaction_info=TransactionInfo(commission_fee, transaction_id),
        )

    def __get_wallet_owner__(self, address: str):
        wallet_owner_id = self.wallet_repository.fetch_wallet_owner_id(address)
        if wallet_owner_id == -1:
            return WalletOwnerResponse(
                status_code=HTTPStatus.NOT_FOUND, message="Wallet not found"
            )
        wallet_owner = self.user_repository.fetch_user_by_id(wallet_owner_id)
        if wallet_owner is None:
            return WalletOwnerResponse(
                status_code=HTTPStatus.NOT_FOUND, message="User not found"
            )
        return WalletOwnerResponse(status_code=HTTPStatus.OK, wallet_owner=wallet_owner)

    def get_user_transactions(self, api_key: str) -> TransactionListResponse:
        user = self.user_repository.fetch_user(api_key)
        if user is None:
            return TransactionListResponse(
                status_code=HTTPStatus.NOT_FOUND, message="User not found"
            )

        transactions: list[ITransaction] = []
        user_wallets = self.wallet_repository.get_user_wallets_address(
            user.get_user_id()
        )
        for wallet_address in user_wallets:
            wallet_transactions = self.transaction_repository.fetch_transactions(
                wallet_address
            )
            if len(wallet_transactions) > 0:
                # transactions.append(wallet_transactions)
                transactions += wallet_transactions

        return TransactionListResponse(
            status_code=HTTPStatus.OK, transactions_list=transactions
        )

    def get_wallet_transactions(
        self, wallet_address: str, api_key: str
    ) -> TransactionListResponse:
        wallet = self.wallet_repository.fetch_wallet(wallet_address)
        if wallet is None:
            return TransactionListResponse(
                status_code=HTTPStatus.NOT_FOUND, message="Wallet not found"
            )

        wallet_owner_id = self.wallet_repository.fetch_wallet_owner_id(wallet_address)
        wallet_owner = self.user_repository.fetch_user_by_id(wallet_owner_id)
        if wallet_owner is not None:
            if wallet_owner.get_api_key() != api_key:
                return TransactionListResponse(
                    status_code=HTTPStatus.FORBIDDEN, message="Api Key not correct"
                )

        transactions = self.transaction_repository.fetch_transactions(wallet_address)

        return TransactionListResponse(
            status_code=HTTPStatus.OK, transactions_list=transactions
        )
