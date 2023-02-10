from http import HTTPStatus

import pytest

from wallet.core.facade import BitcoinWalletService
from wallet.core.observer import DefaultStatisticsObserver
from wallet.core.user.user import UserRequest
from wallet.core.utils import BinanceApiConvertor, KeyGenerator
from wallet.infra.in_memory.statistics_in_memory import StatisticsRepositoryInMemory
from wallet.infra.in_memory.transaction_in_memory import TransactionRepositoryInMemory
from wallet.infra.in_memory.user_in_memory import UserInMemoryRepository
from wallet.infra.in_memory.wallet_in_memory import WalletInMemoryRepository


@pytest.fixture
def service() -> BitcoinWalletService:
    wallet_repository = WalletInMemoryRepository()
    convertor = BinanceApiConvertor()
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


def test_create_wallet(service: BitcoinWalletService) -> None:
    user_request = UserRequest("GG31")
    user = service.create_user(user_request)
    user_info = user.user_info
    assert user_info is not None
    api_key = user_info.api_key
    wallet = service.create_wallet(api_key)
    wallet_info = wallet.wallet_info
    assert wallet_info is not None
    assert wallet.status_code == HTTPStatus.CREATED
    assert wallet_info.btc_balance == 1


def test_create_four_wallets(service: BitcoinWalletService) -> None:
    user_request = UserRequest("GG32")
    user = service.create_user(user_request)
    user_info = user.user_info
    assert user_info is not None
    api_key = user_info.api_key
    for i in range(0, 3):
        wallet = service.create_wallet(api_key)
        wallet_info = wallet.wallet_info
        assert wallet.status_code == HTTPStatus.CREATED
        assert wallet_info is not None
        assert wallet_info.btc_balance == 1
    wallet_information = service.create_wallet(api_key)
    assert wallet_information.status_code == HTTPStatus.UNAUTHORIZED


def test_create_wallet_with_no_user(service: BitcoinWalletService) -> None:
    api_key = "abf#1~defgh$21e@#6c2$1^"
    wallet_info = service.create_wallet(api_key)
    assert wallet_info.status_code == HTTPStatus.FORBIDDEN


def test_get_wallet(service: BitcoinWalletService) -> None:
    user_request = UserRequest("GG33")
    user = service.create_user(user_request)
    user_info = user.user_info
    assert user_info is not None
    api_key = user_info.api_key
    wallet = service.create_wallet(api_key)
    wallet_info = wallet.wallet_info
    assert wallet_info is not None
    wallet_address = wallet_info.wallet_address
    wallet_updated_info = wallet.wallet_info
    assert wallet_updated_info is not None
    assert wallet is not None
    assert wallet_updated_info.wallet_address == wallet_address
    assert wallet_updated_info.btc_balance == 1
    assert wallet.status_code == HTTPStatus.CREATED


def test_get_wallet_with_wrong_input(service: BitcoinWalletService) -> None:
    user_request = UserRequest("GG34")
    user = service.create_user(user_request)
    user_info = user.user_info
    assert user_info is not None
    api_key = user_info.api_key
    wallet = service.create_wallet(api_key)
    wallet_info = wallet.wallet_info
    assert wallet_info is not None
    wallet_address = wallet_info.wallet_address
    assert (
        service.get_wallet(address=wallet_address, api_key="").status_code
        == HTTPStatus.FORBIDDEN
    )
    assert (
        service.get_wallet(address="", api_key=api_key).status_code
        == HTTPStatus.FORBIDDEN
    )
