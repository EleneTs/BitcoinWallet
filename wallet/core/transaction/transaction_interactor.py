from typing import Protocol


class Transaction(Protocol):
    def get_id(self):
        pass

    def get_wallet_from(self):
        pass

    def get_wallet_to(self):
        pass

    def get_amount(self):
        pass
