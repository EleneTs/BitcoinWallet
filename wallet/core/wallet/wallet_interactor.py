from dataclasses import dataclass
from http import HTTPStatus
from typing import Optional, Protocol

from wallet.core.user.user import IUser
from wallet.core.user.user_interactor import UserRepository
from wallet.core.utils import Convertor, Generator
from wallet.core.wallet.wallet import (FetchWalletRequest, WalletInfo,
                                       WalletResponse)

MAX_USER_WALLETS = 3
INITIAL_BTC_BALANCE = 1.0


class WalletRepository(Protocol):
    def count_user_wallets(self, user: IUser) -> int:
        pass

    def create_wallet(
        self, wallet_address: str, btc_balance: float, user: IUser
    ) -> Optional[FetchWalletRequest]:
        pass

    def fetch_wallet(self, wallet_address: str) -> Optional[FetchWalletRequest]:
        pass

    def fetch_wallet_owner_id(self, wallet_address: str) -> int:
        pass

    def make_transaction(self, wallet_address: str, amount: float):
        pass

    def get_user_wallets_address(self, user_id: int) -> list[str]:
        pass


@dataclass
class WalletInteractor:
    wallet_repository: WalletRepository
    user_repository: UserRepository
    convertor: Convertor
    generator: Generator

    def create_wallet(self, api_key: str) -> WalletResponse:

        user = self.user_repository.fetch_user(api_key)
        if not user:
            return WalletResponse(
                status_code=HTTPStatus.FORBIDDEN, message="Invalid credentials"
            )

        if self.wallet_repository.count_user_wallets(user) >= MAX_USER_WALLETS:
            return WalletResponse(
                status_code=HTTPStatus.UNAUTHORIZED,
                message="You have reached the limit of 3 wallets",
            )

        wallet_info = self.wallet_repository.create_wallet(
            self.generator.generate_key(), INITIAL_BTC_BALANCE, user
        )

        assert wallet_info is not None

        return WalletResponse(
            status_code=HTTPStatus.CREATED,
            wallet_info=WalletInfo(
                wallet_info.wallet_address,
                wallet_info.balance,
                self.convertor.get_btc_to_usd(wallet_info.balance),
            ),
        )

    def get_wallet(self, address: str, api_key: str) -> WalletResponse:
        user = self.user_repository.fetch_user(api_key)
        wallet_owner_id = self.wallet_repository.fetch_wallet_owner_id(address)
        if user is None or user.get_user_id() != wallet_owner_id:
            return WalletResponse(
                status_code=HTTPStatus.FORBIDDEN, message="Invalid credentials"
            )

        wallet_info = self.wallet_repository.fetch_wallet(address)
        if wallet_info is None:
            return WalletResponse(
                status_code=HTTPStatus.NOT_FOUND, message="Wallet not found"
            )
        return WalletResponse(
            status_code=HTTPStatus.OK,
            wallet_info=WalletInfo(
                wallet_info.wallet_address,
                wallet_info.balance,
                self.convertor.get_btc_to_usd(wallet_info.balance),
            ),
        )
