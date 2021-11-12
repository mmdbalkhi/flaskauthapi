import hashlib
from typing import AnyStr, Dict


def hash_data(data: Dict, salt="1234") -> str:
    data["salt"] = salt
    hashcode = hashlib.sha3_512(str(data)[::-1].encode("utf8"))
    return hashcode.hexdigest()


def hash_username(username: AnyStr) -> str:
    hashcode = hashlib.sha256(username.encode("utf8"))
    return hashcode.hexdigest()
