from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from wallet.core.facade import BitcoinWalletService
from wallet.core.user.user_interactor import UserRequest
from wallet.core.wallet.wallet import CreateWalletRequest
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
def create_wallet(
    wallet_request: CreateWalletRequest, core: BitcoinWalletService = Depends(get_core)
):
    wallet_response = core.create_wallet(wallet_request)
    if wallet_response.status_code != HTTPStatus.CREATED:
        raise HTTPException(
            status_code=wallet_response.status_code, detail=wallet_response.message
        )
    return wallet_response.wallet_info


@wallet_api.get("/wallets/{address}/")
def get_wallet(address: str, core: BitcoinWalletService = Depends(get_core)):
    wallet_response = core.get_wallet(address=address)
    if wallet_response.status_code != HTTPStatus.OK:
        raise HTTPException(
            status_code=wallet_response.status_code, detail=wallet_response.message
        )
    return wallet_response.wallet_info


@wallet_api.post("/transactions")
def create_transaction(core: BitcoinWalletService = Depends(get_core)):
    return core.create_transaction()


@wallet_api.get("/transactions")
def get_all_transactions(core: BitcoinWalletService = Depends(get_core)):
    return core.get_all_transactions()


@wallet_api.get("/wallets/{address}/transactions")
def get_transactions(core: BitcoinWalletService = Depends(get_core)):
    return core.get_transactions()


@wallet_api.get("/statistics")
def get_statistics(core: BitcoinWalletService = Depends(get_core)):
    return core.get_statistics()
