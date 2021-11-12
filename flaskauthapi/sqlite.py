import sqlite3
from os.path import realpath

from hash import hash_data, hash_username

path = realpath(".") + "/" + "users.db"


def create_table():
    conn = sqlite3.connect(path)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS users (
                username TEXT NOT NULL,
                password TEXT NOT NULL
                );"""
    )

    conn.commit()
    conn.close()


def read_sql(username):
    conn = sqlite3.connect(path)
    password = conn.execute(
        f"""SELECT password FROM users where username in ('{hash_username(username)}');"""
    ).fetchone()
    conn.close()
    return password


def write_sql(username, password):
    conn = sqlite3.connect(path)
    data = {"username": username, "password": password}
    conn.execute(
        f"""INSERT INTO users (username, password) VALUES (
        '{hash_username(username)}',
        '{hash_data(data)}');"""
    )
    conn.commit()
    conn.close()
