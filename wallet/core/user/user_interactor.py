from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus
from typing import Optional, Protocol

from wallet.core.user.user import (FetchUserRequest, IUser, UserInfo,
                                   UserRequest, UserResponse)
from wallet.core.utils import Generator


class UserRepository(Protocol):
    def create_user(self, api_key: str, username: str) -> None:
        pass

    def fetch_user(self, user_api_key: str) -> Optional[IUser]:
        pass

    def contains(self, username) -> bool:
        pass

    def fetch_user_by_id(self, user_id: int) -> Optional[IUser]:
        pass


@dataclass
class UserInteractor:
    user_repository: UserRepository
    generator: Generator

    def create_user(self, user_request: UserRequest) -> UserResponse:
        api_key = self.generator.generate_key()
        if self.user_repository.fetch_user(api_key) is not None:
            return UserResponse(
                status_code=HTTPStatus.FORBIDDEN, message="Invalid api key"
            )
        if self.contains_username(user_request.username):
            return UserResponse(
                status_code=HTTPStatus.CONFLICT, message="Username already exists"
            )
        self.user_repository.create_user(api_key, user_request.username)
        return UserResponse(
            status_code=HTTPStatus.CREATED,
            user_info=UserInfo(api_key),
        )

    def fetch_user(self, request: FetchUserRequest) -> Optional[IUser]:
        user = self.user_repository.fetch_user(request.api_key)
        return user

    def contains_username(self, username: str) -> bool:
        return self.user_repository.contains(username)

    def fetch_user_by_id(self, user_id: int) -> Optional[IUser]:
        return self.user_repository.fetch_user_by_id(user_id)
