import os
import sqlite3

from werkzeug.security import check_password_hash, generate_password_hash

# Always sits next to this file, no matter where the server is started from
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jarvis.db")


def create_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def register_user(username, password):
    """Returns True on success, False if the username is already taken."""
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            'INSERT INTO users (username, password) VALUES (?, ?)',
            (username, generate_password_hash(password)),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def login_user(username, password):
    """Returns True if the username exists and the password matches."""
    conn = sqlite3.connect(DB_PATH)
    try:
        record = conn.execute(
            'SELECT password FROM users WHERE username = ?', (username,)
        ).fetchone()
    finally:
        conn.close()

    return bool(record and check_password_hash(record[0], password))
