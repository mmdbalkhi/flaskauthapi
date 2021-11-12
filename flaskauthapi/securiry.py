import hashlib
from typing import AnyStr, Dict

from config import secret_key


def hash_data(data: Dict, salt=secret_key) -> str:
    data["salt"] = salt
    hashcode = hashlib.sha3_512(str(data)[::-1].encode("utf8"))
    return hashcode.hexdigest()


def hash_username(username: AnyStr) -> str:
    hashcode = hashlib.sha256(username.encode("utf8"))
    return hashcode.hexdigest()


def password_secure(username: AnyStr, password: AnyStr) -> bool:
    if username == password:
        return False
    elif password.isdigit() or len(password) < 8:
        return False

    return True


def check_corrected(username: AnyStr, password: AnyStr) -> bool:
    data = {"username": username, "password": password}
    data_hash = hash_data(data)

    if not read_sql(username):
        return False

    if read_sql(username)[0] == data_hash:
        return True

    return
