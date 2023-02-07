from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from wallet.core.facade import BitcoinWalletService
from wallet.core.transaction.transaction import CreateTransactionRequest
from wallet.core.user.user_interactor import UserRequest
from wallet.infra.fastapi.dependables import get_core

wallet_api = APIRouter()


@wallet_api.post("/users")
def create_user(
    user_request: UserRequest, core: BitcoinWalletService = Depends(get_core)
):
    user_response = core.create_user(user_request)
    if user_response.status_code != HTTPStatus.CREATED:
        raise HTTPException(
            status_code=user_response.status_code, detail=user_response.message
        )
    return user_response.user_info


@wallet_api.post("/wallets")
def create_wallet(api_key: str, core: BitcoinWalletService = Depends(get_core)):
    wallet_response = core.create_wallet(api_key)
    if wallet_response.status_code != HTTPStatus.CREATED:
        raise HTTPException(
            status_code=wallet_response.status_code, detail=wallet_response.message
        )
    return wallet_response.wallet_info


@wallet_api.get("/wallets/{address}/")
def get_wallet(
    address: str, api_key: str, core: BitcoinWalletService = Depends(get_core)
):
    wallet_response = core.get_wallet(address, api_key)
    if wallet_response.status_code != HTTPStatus.OK:
        raise HTTPException(
            status_code=wallet_response.status_code, detail=wallet_response.message
        )
    return wallet_response.wallet_info


@wallet_api.post("/transactions")
def create_transaction(
    transaction_request: CreateTransactionRequest,
    core: BitcoinWalletService = Depends(get_core),
):
    response = core.create_transaction(transaction_request)
    if response.status_code != HTTPStatus.CREATED:
        raise HTTPException(status_code=response.status_code, detail=response.message)
    return response.transaction_info


@wallet_api.get("/transactions")
def get_user_transactions(api_key: str, core: BitcoinWalletService = Depends(get_core)):
    response = core.get_user_transactions(api_key)
    if response.status_code != HTTPStatus.OK:
        raise HTTPException(status_code=response.status_code, detail=response.message)
    return response.transactions_list


@wallet_api.get("/wallets/{address}/transactions")
def get_wallet_transactions(
    address: str, api_key: str, core: BitcoinWalletService = Depends(get_core)
):
    response = core.get_wallet_transactions(address, api_key)
    if response.status_code != HTTPStatus.OK:
        raise HTTPException(status_code=response.status_code, detail=response.message)
    return response.transactions_list


@wallet_api.get("/statistics")
def get_statistics(core: BitcoinWalletService = Depends(get_core)):
    return core.get_statistics()
