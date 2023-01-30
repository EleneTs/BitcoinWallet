from fastapi import FastAPI

from wallet.core.facade import BitcoinWalletService
from wallet.infra.fastapi.wallet_api import wallet_api


def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(wallet_api)
    app.state.core = BitcoinWalletService()

    return app
