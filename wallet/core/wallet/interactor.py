from typing import Protocol


class Wallet(Protocol):
    def get_id(self):
        pass

    def get_address(self):
        pass

    def get_balance(self):
        pass
