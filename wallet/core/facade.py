from dataclasses import dataclass

from wallet.core.observer import StatisticsObserver
from wallet.core.statistics.statistics import StatisticsResponse
from wallet.core.statistics.statistics_interactor import StatisticsInteractor, StatisticsRepository
from wallet.core.transaction.transaction import (CreateTransactionRequest,
                                                 TransactionListResponse,
                                                 TransactionResponse)
from wallet.core.transaction.transaction_interactor import \
    TransactionInteractor
from wallet.core.user.user_interactor import (UserInteractor, UserRepository,
                                              UserRequest, UserResponse)
from wallet.core.utils import Convertor, Generator
from wallet.core.wallet.wallet_interactor import (WalletInteractor,
                                                  WalletResponse)
from wallet.infra.database.transaction_repository import TransactionRepository
from wallet.infra.database.wallet_repository import WalletRepository


@dataclass
class BitcoinWalletService:
    user_interactor: UserInteractor
    wallet_interactor: WalletInteractor
    transaction_interactor: TransactionInteractor
    statistics_interactor: StatisticsInteractor

    @classmethod
    def create(
        cls,
        user_repository: UserRepository,
        wallet_repository: WalletRepository,
        transaction_repository: TransactionRepository,
        statistics_repository: StatisticsRepository,
        convertor: Convertor,
        generator: Generator,
        statistics_observer: StatisticsObserver,
    ) -> "BitcoinWalletService":
        return cls(
            user_interactor=UserInteractor(
                user_repository=user_repository, generator=generator
            ),
            wallet_interactor=WalletInteractor(
                wallet_repository=wallet_repository,
                user_repository=user_repository,
                convertor=convertor,
                generator=generator,
            ),
            transaction_interactor=TransactionInteractor(
                user_repository=user_repository,
                wallet_repository=wallet_repository,
                transaction_repository=transaction_repository,
                statistics_repository=statistics_repository,
                statistics_observer=statistics_observer,
            ),
            statistics_interactor=StatisticsInteractor(
                statistics_repository=statistics_repository
            ),
        )

    def create_user(self, user_request: UserRequest) -> UserResponse:
        return self.user_interactor.create_user(user_request)

    def create_wallet(self, api_key: str) -> WalletResponse:
        return self.wallet_interactor.create_wallet(api_key)

    def get_wallet(self, address: str, api_key: str):
        return self.wallet_interactor.get_wallet(address, api_key)

    def create_transaction(
        self, transaction_request: CreateTransactionRequest
    ) -> TransactionResponse:
        return self.transaction_interactor.create_transaction(transaction_request)

    def get_user_transactions(self, api_key: str) -> TransactionListResponse:
        return self.transaction_interactor.get_user_transactions(api_key)

    def get_wallet_transactions(self, address: str, api_key: str):
        return self.transaction_interactor.get_wallet_transactions(address, api_key)

    def get_statistics(self, admin_api_key: str) -> StatisticsResponse:
        return self.statistics_interactor.get_statistics(admin_api_key)
