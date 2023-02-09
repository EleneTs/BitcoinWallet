from http import HTTPStatus

import pytest

from wallet.core.facade import BitcoinWalletService
from wallet.core.observer import DefaultStatisticsObserver
from wallet.core.transaction.transaction import CreateTransactionRequest
from wallet.core.user.user import UserRequest
from wallet.core.utils import CoinApiConvertor, KeyGenerator
from wallet.infra.in_memory.statistics_in_memory import StatisticsRepositoryInMemory
from wallet.infra.in_memory.transaction_in_memory import TransactionRepositoryInMemory
from wallet.infra.in_memory.user_in_memory import UserInMemoryRepository
from wallet.infra.in_memory.wallet_in_memory import WalletInMemoryRepository

ADMIN_API_KEY = "1d95d3aa5dcd48189edc62582cc9c288"
COMMISSION_FEE = 0.015


@pytest.fixture
def service() -> BitcoinWalletService:
    wallet_repository = WalletInMemoryRepository()
    convertor = CoinApiConvertor()
    generator = KeyGenerator()
    observer = DefaultStatisticsObserver()
    transaction_repository = TransactionRepositoryInMemory()
    user_repository = UserInMemoryRepository()
    statistics_repository = StatisticsRepositoryInMemory()
    return BitcoinWalletService.create(
        user_repository=user_repository,
        wallet_repository=wallet_repository,
        transaction_repository=transaction_repository,
        statistics_repository=statistics_repository,
        convertor=convertor,
        generator=generator,
        statistics_observer=observer,
    )


def test_empty_statistics(service: BitcoinWalletService) -> None:
    statistics = service.statistics_interactor.get_statistics(ADMIN_API_KEY)
    assert statistics.status_code == HTTPStatus.OK
    assert statistics.statistics_info.platform_profit == 0
    assert statistics.statistics_info.transactions_count == 0


def test_wrong_admin_key(service: BitcoinWalletService) -> None:
    statistics = service.statistics_interactor.get_statistics("0000000")
    assert statistics.status_code == HTTPStatus.FORBIDDEN


def test_statistics_no_profit(service: BitcoinWalletService) -> None:
    user_request = UserRequest("username1")
    user = service.create_user(user_request)
    api_key = user.user_info.api_key
    wallet_1_info = service.create_wallet(api_key)
    wallet_2_info = service.create_wallet(api_key)
    transaction_request = CreateTransactionRequest(api_key,
                                                   wallet_1_info.wallet_info.wallet_address,
                                                   wallet_2_info.wallet_info.wallet_address,
                                                   0.5)
    service.create_transaction(transaction_request)

    statistics = service.statistics_interactor.get_statistics(ADMIN_API_KEY)
    assert statistics.status_code == HTTPStatus.OK
    assert statistics.statistics_info.platform_profit == 0
    assert statistics.statistics_info.transactions_count == 1


def test_statistics_profit(service: BitcoinWalletService) -> None:
    user_1_request = UserRequest("username1")
    user_1 = service.create_user(user_1_request)
    api_key_1 = user_1.user_info.api_key

    user_2_request = UserRequest("username2")
    user_2 = service.create_user(user_2_request)
    api_key_2 = user_2.user_info.api_key

    wallet_1_info = service.create_wallet(api_key_1)
    wallet_2_info = service.create_wallet(api_key_2)
    transaction_request = CreateTransactionRequest(api_key_1,
                                                   wallet_1_info.wallet_info.wallet_address,
                                                   wallet_2_info.wallet_info.wallet_address,
                                                   0.5)
    service.create_transaction(transaction_request)

    statistics = service.statistics_interactor.get_statistics(ADMIN_API_KEY)
    assert statistics.status_code == HTTPStatus.OK
    assert statistics.statistics_info.platform_profit == (0.5 * COMMISSION_FEE)
