from dataclasses import dataclass

from wallet.core.user.interactor import UserInteractor
from wallet.infra.database.transaction_repository import TransactionRepository
from wallet.infra.database.user_repository import UserRepositoryDb
from wallet.infra.database.wallet_repository import WalletRepository


@dataclass
class BitcoinWalletService:
    user_interactor: UserInteractor

    @classmethod
    def create(
        cls,
        user_repository: UserRepositoryDb,
        wallet_repository: WalletRepository,
        transaction_repository: TransactionRepository,
    ) -> "BitcoinWalletService":
        return cls(
            user_interactor=UserInteractor(user_repository=user_repository)
        )

    def create_user(self) -> str:
        return self.user_interactor.create_user()

    def create_wallet(self):
        pass

    def get_wallet(self):
        pass

    def create_transaction(self):
        pass

    def get_all_transactions(self):
        pass

    def get_transactions(self):
        pass

    def get_statistics(self):
        pass
