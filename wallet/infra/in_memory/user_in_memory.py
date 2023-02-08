from dataclasses import dataclass, field
from typing import List, Optional

from wallet.core.user.user import IUser, User


@dataclass
class UserInMemoryRepository:
    users: List[User] = field(default_factory=list)

    def create_user(self, api_key: str, username: str) -> None:
        generated_id = len(self.users) + 1
        self.users.append(User(generated_id, api_key, username))

    def fetch_user(self, api_key: str) -> Optional[IUser]:
        for user in self.users:
            if user.get_api_key() == api_key:
                return user
        return None

    def contains(self, username: str) -> bool:
        for user in self.users:
            if user.get_username() == username:
                return True
        return False

    def fetch_user_by_id(self, user_id: int) -> Optional[IUser]:
        for user in self.users:
            if user.get_user_id() == user_id:
                return user
        return None
