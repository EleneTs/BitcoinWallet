from sqlite3 import Connection, Cursor, connect


class UserRepository:
    def __init__(self, database_name: str) -> None:
        self.db_name = database_name
        con: Connection = connect(self.db_name)
        cursor: Cursor = con.cursor()
        self.create_users_table(cursor)
        con.commit()
        con.close()

    def create_users_table(self, cursor: Cursor):
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY,
               username TEXT NOT NULL UNIQUE,
               api_key TEXT NOT NULL UNIQUE);"""
        )
