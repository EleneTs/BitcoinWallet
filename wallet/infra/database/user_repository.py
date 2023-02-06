from sqlite3 import connect
from typing import Optional

from wallet.core.user.interactor import User, UserRepository


class UserRepositoryDb(UserRepository):
    def __init__(self, database_name: str) -> None:
        self.db_name = database_name
        self.create_users_table()

    def create_users_table(self):
        con = connect(self.db_name)
        cursor = con.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
               username TEXT NOT NULL UNIQUE,
               api_key TEXT NOT NULL UNIQUE);"""
        )

    def create_user(self, api_key: str, username: str) -> None:
        con = connect(self.db_name)
        cursor = con.cursor()
        cursor.execute("INSERT INTO users (username, api_key) VALUES (?,?)", (username, api_key,))
        con.commit()
        con.close()

    def fetch_user(self, api_key: str) -> Optional[User]:
        con = connect(self.db_name)
        cursor = con.cursor()
        cursor.execute("SELECT * from users WHERE api_key = ?", (api_key,))
        result = cursor.fetchone()
        con.close()
        if result:
            username = result[0]
            api_key = result[1]
            return User(username=username, api_key=api_key)
        else:
            return None

    def contains(self, username: str) -> bool:
        con = connect(self.db_name)
        cursor = con.cursor()
        cursor.execute("SELECT * from users WHERE username = ?", (username,))
        result = cursor.fetchone()
        con.close()
        if result:
            return True
        else:
            return False
