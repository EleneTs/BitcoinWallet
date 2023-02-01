from typing import Protocol


class User(Protocol):
    def get_id(self):
        pass

    def get_username(self):
        pass

    def get_api_key(self):
        pass
