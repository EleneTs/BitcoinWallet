from dataclasses import dataclass

from wallet.infra.database.transaction_repository import TransactionRepository
from wallet.infra.database.user_repository import UserRepository
from wallet.infra.database.wallet_repository import WalletRepository


@dataclass
class BitcoinWalletService:

    @classmethod
    def create(
            cls,
            user_repository: UserRepository,
            wallet_repository: WalletRepository,
            transaction_repository: TransactionRepository,
    ) -> "BitcoinWalletService":
        pass

    def create_user(self):
        pass

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

