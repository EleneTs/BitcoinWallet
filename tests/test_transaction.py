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


def test_transaction_between_one_user(service: BitcoinWalletService) -> None:
    user_request = UserRequest("username1")
    user = service.create_user(user_request)
    api_key = user.user_info.api_key
    wallet_1_info = service.create_wallet(api_key)
    wallet_2_info = service.create_wallet(api_key)
    transaction_request = CreateTransactionRequest(api_key,
                                                   wallet_1_info.wallet_info.wallet_address,
                                                   wallet_2_info.wallet_info.wallet_address,
                                                   0.5)
    response = service.create_transaction(transaction_request)
    assert service.get_wallet(address=wallet_1_info.wallet_info.wallet_address,
                              api_key=api_key).wallet_info.btc_balance == 0.5
    assert service.get_wallet(address=wallet_2_info.wallet_info.wallet_address,
                              api_key=api_key).wallet_info.btc_balance == 1.5
    assert response.status_code == HTTPStatus.CREATED
    assert response.transaction_info.commission_fee == 0


def test_transaction_between_different_users(service: BitcoinWalletService) -> None:
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
    response = service.create_transaction(transaction_request)
    full_transaction_amount = 0.5 + (0.5 * COMMISSION_FEE)

    assert service.get_wallet(address=wallet_1_info.wallet_info.wallet_address,
                              api_key=api_key_1).wallet_info.btc_balance == (1 - full_transaction_amount)
    assert service.get_wallet(address=wallet_2_info.wallet_info.wallet_address,
                              api_key=api_key_2).wallet_info.btc_balance == 1.5
    assert response.status_code == HTTPStatus.CREATED
    assert response.transaction_info.commission_fee == (0.5 * COMMISSION_FEE)


def test_get_user_transactions(service: BitcoinWalletService) -> None:
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

    response = service.get_user_transactions(api_key)
    assert response.status_code == HTTPStatus.OK
    assert len(response.transactions_list) == 2


def test_get_wallet_transactions(service: BitcoinWalletService) -> None:
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

    response = service.get_wallet_transactions(wallet_1_info.wallet_info.wallet_address,
                                               api_key)
    assert response.status_code == HTTPStatus.OK
    assert len(response.transactions_list) == 1


def test_get_transactions_invalid_data(service: BitcoinWalletService) -> None:
    response_wallet = service.get_wallet_transactions("",
                                                      "")
    response_user = service.get_user_transactions("")

    assert response_wallet.status_code == HTTPStatus.NOT_FOUND
    assert response_user.status_code == HTTPStatus.NOT_FOUND


def test_transaction_not_enough_balance(service: BitcoinWalletService) -> None:
    user_request = UserRequest("username1")
    user = service.create_user(user_request)
    api_key = user.user_info.api_key
    wallet_1_info = service.create_wallet(api_key)
    wallet_2_info = service.create_wallet(api_key)
    transaction_request = CreateTransactionRequest(api_key,
                                                   wallet_1_info.wallet_info.wallet_address,
                                                   wallet_2_info.wallet_info.wallet_address,
                                                   1.1)
    response = service.create_transaction(transaction_request)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_transaction_between_one_wallet(service: BitcoinWalletService) -> None:
    user_request = UserRequest("username1")
    user = service.create_user(user_request)
    api_key = user.user_info.api_key
    wallet_info = service.create_wallet(api_key)

    transaction_request = CreateTransactionRequest(api_key,
                                                   wallet_info.wallet_info.wallet_address,
                                                   wallet_info.wallet_info.wallet_address,
                                                   0.5)
    response = service.create_transaction(transaction_request)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_transaction_invalid_credentials_empty(service: BitcoinWalletService) -> None:
    transaction_request = CreateTransactionRequest("",
                                                   "",
                                                   "",
                                                   0.5)
    response = service.create_transaction(transaction_request)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_transaction_invalid_credentials(service: BitcoinWalletService) -> None:
    user_request = UserRequest("username1")
    user = service.create_user(user_request)
    api_key = user.user_info.api_key
    wallet_1_info = service.create_wallet(api_key)
    wallet_2_info = service.create_wallet(api_key)

    transaction_request = CreateTransactionRequest("000000000",
                                                   wallet_1_info.wallet_info.wallet_address,
                                                   wallet_2_info.wallet_info.wallet_address,
                                                   0.5)
    response = service.create_transaction(transaction_request)
    assert response.status_code == HTTPStatus.BAD_REQUEST
