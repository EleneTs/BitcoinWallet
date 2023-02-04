from sqlite3 import Connection, Cursor, connect
from typing import Optional

from wallet.core.user.interactor import UserRepository, User

# class UserRepositoryDb(UserRepository):
#     cursor: Cursor
#     connection: Connection
#
#     def __init__(self, database_name: str) -> None:
#         self.db_name = database_name
#         con: Connection = connect(self.db_name)
#         cursor: Cursor = con.cursor()
#         self.create_users_table(cursor)
#         con.commit()
#         con.close()
#
#     def create_users_table(self, cursor: Cursor):
#         cursor.execute(
#             """CREATE TABLE IF NOT EXISTS users (
#                id INTEGER PRIMARY KEY,
#                username TEXT NOT NULL UNIQUE,
#                api_key TEXT NOT NULL UNIQUE);"""
#         )
#

class UserRepositoryDb(UserRepository):
    def __init__(self, database_name: str) -> None:
        self.db_name = database_name
        self.create_users_table()

    def create_users_table(self):
        con = connect(self.db_name)
        cursor = con.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
               api_key TEXT NOT NULL UNIQUE);"""
        )

    def create_user(self, api_key: str) -> None:
        con = connect(self.db_name)
        cursor = con.cursor()
        cursor.execute("INSERT INTO users (api_key) VALUES (?)", (api_key,))
        con.commit()
        con.close()

    def fetch_user(self, api_key: str) -> Optional[User]:
        con = connect(self.db_name)
        cursor = con.cursor()
        cursor.execute("SELECT * from users WHERE api_key = ?", (api_key,))
        result = cursor.fetchone()
        con.close()
        if result:
            api_key = result
            return User(api_key=api_key)
        else:
            return None
