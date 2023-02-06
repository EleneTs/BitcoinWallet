from dataclasses import dataclass

from wallet.core.user.user_interactor import UserInteractor, UserRequest, UserResponse
from wallet.core.wallet.wallet_interactor import WalletInteractor, WalletResponse
from wallet.infra.btc_usd_conversion import Convertor
from wallet.infra.database.transaction_repository import TransactionRepository
from wallet.infra.database.user_repository import UserRepositoryDb
from wallet.infra.database.wallet_repository import WalletRepository


@dataclass
class BitcoinWalletService:
    user_interactor: UserInteractor
    wallet_interactor: WalletInteractor

    @classmethod
    def create(
        cls,
        user_repository: UserRepositoryDb,
        wallet_repository: WalletRepository,
        transaction_repository: TransactionRepository,
        convertor: Convertor,
    ) -> "BitcoinWalletService":
        return cls(
            user_interactor=UserInteractor(user_repository=user_repository),
            wallet_interactor=WalletInteractor(
                wallet_repository=wallet_repository,
                user_repository=user_repository,
                convertor=convertor,
            ),
        )

    def create_user(self, user_request: UserRequest) -> UserResponse:
        return self.user_interactor.create_user(user_request)

    def create_wallet(self, api_key: str) -> WalletResponse:
        return self.wallet_interactor.create_wallet(api_key)

    def get_wallet(self, address):
        return self.wallet_interactor.get_wallet(address)

    def create_transaction(self):
        pass

    def get_all_transactions(self):
        pass

    def get_transactions(self):
        pass

    def get_statistics(self):
        pass
