import sqlite3
import time
from config import Config

conn = sqlite3.connect(Config.DB_PATH, check_same_thread=False)
conn.row_factory = sqlite3.Row


def init_db():
    """
    Создание таблиц в базе данных
    """
    with open("app/schema.sql") as f:
        conn.executescript(f.read())
    conn.commit()


# ---- users ----

def get_any_user() -> sqlite3.Row | None:
    cur = conn.execute("SELECT * FROM users LIMIT 1")
    return cur.fetchone()


def create_user(username: str):
    conn.execute(
        "INSERT INTO users (username) VALUES (?)", (username,)
    )
    conn.commit()


# ---- auth codes ----

def save_auth_code(code: str, user_id: int, ttl: int):
    conn.execute(
        "INSERT INTO oauth_codes VALUES (?, ?, ?)",
        (code, user_id, int(time.time()) + ttl),
    )
    conn.commit()


def pop_auth_code(code: str):
    cur = conn.execute(
        "SELECT user_id, expires_at FROM oauth_codes WHERE code = ?", (code,)
    )
    row = cur.fetchone()

    if not row or row["expires_at"] < time.time():
        return None

    conn.execute("DELETE FROM oauth_codes WHERE code = ?", (code,))
    conn.commit()

    return row["user_id"]


# ---- access tokens ----

def save_access_token(token: str, user_id: int, ttl: int):
    conn.execute(
        "INSERT INTO access_tokens VALUES (?, ?, ?)",
        (token, user_id, int(time.time()) + ttl),
    )
    conn.commit()


def validate_access_token(token: str) -> bool:
    cur = conn.execute(
        "SELECT user_id, expires_at FROM access_tokens WHERE token = ?", (token,)
    )
    row = cur.fetchone()

    if not row or row["expires_at"] < time.time():
        return False

    return True
