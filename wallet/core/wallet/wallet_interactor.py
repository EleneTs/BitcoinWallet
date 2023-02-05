import uuid
from dataclasses import dataclass
from http import HTTPStatus

from wallet.core.user.interactor import UserRepository
from wallet.core.wallet.wallet import WalletInfo, WalletResponse
from wallet.infra.btc_usd_conversion import Convertor
from wallet.infra.database.wallet_repository import WalletRepository

MAX_USER_WALLETS = 3
INITIAL_BTC_BALANCE = 1.0


@dataclass
class WalletInteractor:
    wallet_repository: WalletRepository
    user_repository: UserRepository
    convertor: Convertor

    def create_wallet(self, api_key) -> WalletResponse:

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
            self.generate_wallet_address(), INITIAL_BTC_BALANCE, user
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

    def get_wallet(self, address):
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

    def generate_wallet_address(self):
        return str(uuid.uuid4().hex)
