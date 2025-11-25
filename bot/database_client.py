import sqlite3
import os
import json
from dotenv import load_dotenv

load_dotenv()

def recreate_database() -> None:
    connection = sqlite3.connect(os.getenv("SQLITE_DATABASE_PATH"))
    with connection:
        connection.execute("DROP TABLE IF EXISTS telegram_updates")
        connection.execute(
            """
            CREATE TABLE telegram_updates
            (
                id INTEGER PRIMARY KEY,
                payload TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXIST users
            (
                id INTEGER PRIMARY KEY,
                telegram_id INTEGER NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                state TEXT DEFAULT NULL,
                order_json TEXT DEFAULT NULL
            )
            """,
            )
    
def persist_updates(updates: list) -> None:
    if not updates:
        return
        
    connection = sqlite3.connect(os.getenv("SQLITE_DATABASE_PATH"))
    with connection:
        data = []
        for update in updates:
            pretty_json = json.dumps(update, ensure_ascii=False, indent=2, sort_keys=True)
            data.append((pretty_json,))
        
        connection.executemany(
            "INSERT INTO telegram_updates (payload) VALUES (?)",
            data,
        )
    connection.close()

    def ensure_user_exists(telegram_id: int)->None:
        """Ensure a user with the given telegram_id exists in the users table.
        If the user doesn't exist, create them. All operations happen in a single transactive"""
        with connection:
            cursor = connection.execute(
                "SELECT 1 FROM users WHERE telegram_id = ?",(telegram_id,)
            )
        if cursor.fetchone() is None:
            connection.execute(
                "INSERT INTO users(telegram_id) VALUES(?)", (telegram_id,)
            )