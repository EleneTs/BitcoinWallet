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
    statistics_info = statistics.statistics_info
    assert statistics_info is not None
    assert statistics.status_code == HTTPStatus.OK
    assert statistics_info.platform_profit == 0
    assert statistics_info.transactions_count == 0


def test_wrong_admin_key(service: BitcoinWalletService) -> None:
    statistics = service.statistics_interactor.get_statistics("0000000")
    assert statistics.status_code == HTTPStatus.FORBIDDEN


def test_statistics_no_profit(service: BitcoinWalletService) -> None:
    user_request = UserRequest("username1")
    user = service.create_user(user_request)
    user_info = user.user_info
    assert user_info is not None
    api_key = user_info.api_key
    wallet_1_info = service.create_wallet(api_key).wallet_info
    wallet_2_info = service.create_wallet(api_key).wallet_info
    assert wallet_1_info is not None
    assert wallet_2_info is not None
    transaction_request = CreateTransactionRequest(
        api_key,
        wallet_1_info.wallet_address,
        wallet_2_info.wallet_address,
        0.5,
    )
    service.create_transaction(transaction_request)

    statistics = service.statistics_interactor.get_statistics(ADMIN_API_KEY)
    statistics_info = statistics.statistics_info
    assert statistics_info is not None
    assert statistics.status_code == HTTPStatus.OK
    assert statistics_info.platform_profit == 0
    assert statistics_info.transactions_count == 1


def test_statistics_profit(service: BitcoinWalletService) -> None:
    user_1_request = UserRequest("username1")
    user_1 = service.create_user(user_1_request)
    user1_info = user_1.user_info
    assert user1_info is not None
    api_key_1 = user1_info.api_key

    user_2_request = UserRequest("username2")
    user_2 = service.create_user(user_2_request)
    user_2_info = user_2.user_info
    assert user_2_info is not None
    api_key_2 = user_2_info.api_key

    wallet_1_info = service.create_wallet(api_key_1).wallet_info
    wallet_2_info = service.create_wallet(api_key_2).wallet_info
    assert wallet_1_info is not None
    assert wallet_2_info is not None
    transaction_request = CreateTransactionRequest(
        api_key_1,
        wallet_1_info.wallet_address,
        wallet_2_info.wallet_address,
        0.5,
    )
    service.create_transaction(transaction_request)

    statistics = service.statistics_interactor.get_statistics(ADMIN_API_KEY)
    statistics_info = statistics.statistics_info
    assert statistics_info is not None
    assert statistics.status_code == HTTPStatus.OK
    assert statistics_info.platform_profit == (0.5 * COMMISSION_FEE)
