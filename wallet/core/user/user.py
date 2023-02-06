from dataclasses import dataclass, field
from http import HTTPStatus
from typing import Optional, Protocol


class IUser(Protocol):
    def get_user_id(self) -> int:
        pass

    def get_api_key(self) -> str:
        pass

    def get_username(self) -> str:
        pass


@dataclass
class User(IUser):
    id: int
    api_key: str
    username: str

    def get_user_id(self) -> int:
        return self.id

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
