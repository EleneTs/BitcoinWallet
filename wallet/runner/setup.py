from sqlite3 import connect

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
    connection = connect(DB_NAME, check_same_thread=False)
    cursor = connection.cursor()

    user_repository = UserRepositoryDb(connection=connection, cursor=cursor)
    wallet_repository = WalletRepository(connection=connection, cursor=cursor)
    transaction_repository = TransactionRepository(connection=connection, cursor=cursor)
    convertor = CoinApiConvertor()
    app.state.core = BitcoinWalletService.create(
        user_repository=user_repository,
        wallet_repository=wallet_repository,
        transaction_repository=transaction_repository,
        convertor=convertor,
    )
    return app
