from sqlite3 import connect

from fastapi import FastAPI

from wallet.core.facade import BitcoinWalletService
from wallet.core.observer import DefaultStatisticsObserver
from wallet.core.utils import CoinApiConvertor, KeyGenerator
from wallet.infra.database.statistics_repository import StatisticsRepositoryDB
from wallet.infra.database.transaction_repository import \
    TransactionRepositoryDb
from wallet.infra.database.user_repository import UserRepositoryDb
from wallet.infra.database.wallet_repository import WalletRepositoryDb
from wallet.infra.fastapi.wallet_api import wallet_api

DB_NAME = "wallet.db"


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(wallet_api)
    connection = connect(DB_NAME, check_same_thread=False)
    cursor = connection.cursor()

    user_repository = UserRepositoryDb(connection=connection, cursor=cursor)
    wallet_repository = WalletRepositoryDb(connection=connection, cursor=cursor)
    transaction_repository = TransactionRepositoryDb(
        connection=connection, cursor=cursor
    )
    statistics_repository = StatisticsRepositoryDB(
        connection=connection, cursor=cursor
    )
    convertor = CoinApiConvertor()
    generator = KeyGenerator()
    observer = DefaultStatisticsObserver()
    app.state.core = BitcoinWalletService.create(
        user_repository=user_repository,
        wallet_repository=wallet_repository,
        transaction_repository=transaction_repository,
        statistics_repository=statistics_repository,
        convertor=convertor,
        generator=generator,
        statistics_observer=observer,
    )
    return app