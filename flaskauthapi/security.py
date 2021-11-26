import hashlib
from typing import AnyStr, Dict

from config import secret_key
from sqlite import read_sql_v1


def hash_data_v1(data: Dict, salt=secret_key) -> str:
    data["salt"] = salt
    hashcode = hashlib.sha3_512(str(data)[::-1].encode("utf8"))
    return hashcode.hexdigest()


def hash_username_v1(username: AnyStr) -> str:
    hashcode = hashlib.sha256(username.encode("utf8"))
    return hashcode.hexdigest()


def password_secure_v1(username: AnyStr, password: AnyStr) -> bool:
    if username == password:
        return False
    elif password.isdigit() or len(password) < 8:
        return False

    return True


def check_corrected_v1(username: AnyStr, password: AnyStr) -> bool:
    data = {"username": username, "password": password}
    data_hash = hash_data_v1(data)

    if not read_sql_v1(username):
        return False

    if read_sql_v1(username)[0] == data_hash:
        return True

    return
