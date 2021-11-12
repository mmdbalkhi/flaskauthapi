#! env/bin/python
""" an api application for secure auth users
"""

import sys
from typing import AnyStr
from uuid import uuid4

from flask import Flask, jsonify, request

from hash import hash_data, hash_username
from sqlite import create_table, read_sql, write_sql

app = Flask(__name__)
app.secret_key = "wj# 5.7R_bvP<oR mNahq8h~!wU;'\""


secret_key = app.secret_key
if not secret_key:
    print(
        "ERROR: we Can not Find secret_key. "
        "Please Add secret_key For Your App and Run Again."
    )
    sys.exit(1)


def check_corrected(username: AnyStr, password: AnyStr) -> bool:
    data = {"username": username, "password": password}
    data_hash = hash_data(data)

    if not read_sql(username):
        return False

    if read_sql(username)[0] == data_hash:
        return True

    return


@app.route("/signup", methods=["POST"])
def signup():
    """get user informetion and write hashed data to db
    * users can only send post request
    signup ::= username : str, password : str, email/phone(optioal) : str
    """
    try:
        username = request.form["username"]
        password = request.form["password"]
    except KeyError:
        return jsonify({"status": "faile", "msg": "incorrect username or password"})

    write_sql(username, password)
    return jsonify({"status": "ok", "msg": "user created"})


@app.route("/login", methods=["POST"])
def login():
    """get sended datas from user and check"""
    try:
        username = request.form["username"]
        password = request.form["password"]
    except KeyError:
        return jsonify({"status": "faile", "msg": "incorrect username or password"})

    if check_corrected(username, password):
        return jsonify({"status": "ok", "msg": f"accese Grante for {username}"})

    return jsonify({"status": "faile", "msg": "incorrect username or password"})


# TODO: جلوگیری از تکراری شدن نوشته ها
if __name__ == "__main__":
    create_table()
    app.run("localhost", 5000, True)
