from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Optional, Protocol


class User(Protocol):
    def get_api_key(self) -> str:
        pass


@dataclass
class User(User):
    api_key: str

    def get_api_key(self) -> str:
        return self.api_key


@dataclass
class FetchUserRequest:
    api_key: str


class UserRepository(Protocol):
    def create_user(self, api_key: str) -> None:
        pass

    def fetch_user(self, user_api_key: str) -> Optional[User]:
        pass


@dataclass
class UserInteractor:
    user_repository: UserRepository

    def generate_api_key(self):
        return str(uuid.uuid4().hex)

    def create_user(self) -> str:
        api_key = self.generate_api_key()
        self.user_repository.create_user(api_key)
        return api_key

    def fetch_user(self, request: FetchUserRequest) -> Optional[User]:
        user = self.user_repository.fetch_user(user_api_key=request.api_key)
        return user
