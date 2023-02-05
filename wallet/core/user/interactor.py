from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from http import HTTPStatus
from typing import Optional, Protocol


class User(Protocol):
    def get_api_key(self) -> str:
        pass


@dataclass
class User(User):
    api_key: str
    username: str

    def get_api_key(self) -> str:
        return self.api_key

    def get_username(self) -> str:
        return self.username


@dataclass
class Response:
    message: str = ""
    status_code: int = HTTPStatus.OK


@dataclass
class UserInfo:
    api_key: str = ""


@dataclass
class UserResponse(Response):
    user_info: Optional[UserInfo] = field(default_factory=lambda: UserInfo())


@dataclass
class FetchUserRequest:
    api_key: str


@dataclass
class UserRequest:
    username: str


class UserRepository(Protocol):
    def create_user(self, api_key: str, username: str) -> None:
        pass

    def fetch_user(self, user_api_key: str) -> Optional[User]:
        pass

    def contains(self, username) -> bool:
        pass


@dataclass
class UserInteractor:
    user_repository: UserRepository

    def generate_api_key(self) -> str:
        return str(uuid.uuid4().hex)

    def create_user(self, user_request: UserRequest) -> UserResponse:
        api_key = self.generate_api_key()
        if self.user_repository.fetch_user(api_key) is not None:
            return UserResponse(status_code=HTTPStatus.FORBIDDEN, message="Invalid api key")
        if self.contains_username(user_request.username):
            return UserResponse(status_code=HTTPStatus.CONFLICT, message="Username already exists")
        self.user_repository.create_user(api_key, user_request.username)
        return UserResponse(status_code=HTTPStatus.CREATED,
                            user_info=UserInfo(
                                api_key
                            ), )

    def fetch_user(self, request: FetchUserRequest) -> Optional[User]:
        user = self.user_repository.fetch_user(user_api_key=request.api_key)
        return user

    def contains_username(self, username: str) -> bool:
        return self.user_repository.contains(username)
