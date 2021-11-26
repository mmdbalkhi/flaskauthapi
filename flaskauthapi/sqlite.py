import sqlite3
from os.path import realpath

from security import hash_data_v1, hash_username_v1

path = realpath(".") + "/" + "users.db"


def create_table_v1():
    conn = sqlite3.connect(path)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS users (
                username TEXT NOT NULL,
                password TEXT NOT NULL
                );"""
    )

    conn.commit()
    conn.close()


def read_sql_v1(username):
    conn = sqlite3.connect(path)
    password = conn.execute(
        f"""SELECT password FROM users
        where username in ('{hash_username_v1(username)}');"""
    ).fetchone()
    conn.close()
    return password


def read_username_from_sql_v1(username):
    conn = sqlite3.connect(path)
    password = conn.execute(
        f"""SELECT username FROM users
        where username in ('{hash_username_v1(username)}');"""
    ).fetchone()
    conn.close()
    return password


def write_sql_v1(username, password):
    conn = sqlite3.connect(path)
    data = {"username": username, "password": password}
    conn.execute(
        f"""INSERT INTO users (username, password) VALUES (
        '{hash_username_v1(username)}',
        '{hash_data_v1(data)}');"""
    )
    conn.commit()
    conn.close()
