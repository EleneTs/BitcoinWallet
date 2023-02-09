from sqlite3 import Connection, Cursor
from typing import Optional

from wallet.core.user.user import IUser, User
from wallet.core.user.user_interactor import UserRepository


class UserRepositoryDb(UserRepository):
    def __init__(self, cursor: Cursor, connection: Connection) -> None:
        self.cursor = cursor
        self.connection = connection
        self._create_users_table_()

    def _create_users_table_(self) -> None:
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT NOT NULL UNIQUE,
               api_key TEXT NOT NULL UNIQUE);"""
        )

    def create_user(self, api_key: str, username: str) -> None:
        self.cursor.execute(
            "INSERT INTO users (username, api_key) VALUES (?,?)",
            (
                username,
                api_key,
            ),
        )
        self.connection.commit()

    def fetch_user(self, api_key: str) -> Optional[IUser]:
        self.cursor.execute("SELECT * from users WHERE api_key = ?", (api_key,))
        result = self.cursor.fetchone()
        if result:
            id = result[0]
            username = result[1]
            api_key = result[2]
            return User(id=id, username=username, api_key=api_key)
        else:
            return None

    def contains(self, username: str) -> bool:
        self.cursor.execute("SELECT * from users WHERE username = ?", (username,))
        result = self.cursor.fetchone()
        if result:
            return True
        else:
            return False

    def fetch_user_by_id(self, user_id: int) -> Optional[IUser]:
        self.cursor.execute("SELECT * from users WHERE id = ?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            id = result[0]
            username = result[1]
            api_key = result[2]
            return User(id=id, username=username, api_key=api_key)
        else:
            return None
