from fastapi import FastAPI

from wallet.core.facade import BitcoinWalletService
from wallet.infra.btc_usd_conversion import CoinApiConvertor
from wallet.infra.database.transaction_repository import TransactionRepository
from wallet.infra.database.user_repository import UserRepositoryDb
from wallet.infra.database.wallet_repository import WalletRepository
from wallet.infra.fastapi.wallet_api import wallet_api

DB_NAME = "wallet.db"


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(wallet_api)
    user_repository = UserRepositoryDb(DB_NAME)
    wallet_repository = WalletRepository(DB_NAME)
    transaction_repository = TransactionRepository(DB_NAME)
    convertor = CoinApiConvertor()
    app.state.core = BitcoinWalletService.create(
        user_repository=user_repository,
        wallet_repository=wallet_repository,
        transaction_repository=transaction_repository,
        convertor=convertor,
    )
    return app
