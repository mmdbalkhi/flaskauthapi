#! env/bin/python
""" an api application for secure auth users
"""

import sys
from typing import AnyStr

from config import secret_key
from flask import Flask, jsonify, request
from securiry import check_corrected, hash_data, password_secure
from sqlite import create_table, read_sql, read_username_from_sql, write_sql

app = Flask(__name__)
app.secret_key = secret_key


secret_key = app.secret_key
if not secret_key:
    print(
        "ERROR: we Can not Find secret_key. "
        "Please Add secret_key For config.py and Run Again."
    )
    sys.exit(1)


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
        return (
            jsonify({"status": "error", "msg": "arg(s) are wrong or incomplete"}),
            400,
        )
    if read_username_from_sql(username):
        return jsonify(
            {
                "status": "duplicate",
                "msg": "username already registred",
            }
        )
    if not password_secure(username, password):
        return (
            jsonify(
                {
                    "status": "not secure",
                    "msg": "passoword not secure",
                }
            ),
            406,
        )
    write_sql(username, password)
    return jsonify({"status": "ok", "msg": "user created"})


@app.route("/login", methods=["POST"])
def login():
    """get sended datas from user and check"""
    try:
        username = request.form["username"]
        password = request.form["password"]
    except KeyError:
        return (
            jsonify({"status": "error", "msg": "(s) are wrong or incomplete"}),
            405,
        )

    if check_corrected(username, password):
        return jsonify({"status": "ok", "msg": f"accesse Grante for {username}"}), 406

    return jsonify({"status": "faile", "msg": "incorrect username or password"})


if __name__ == "__main__":
    create_table()
    app.run(host="localhost", port=5000, debug=False)
