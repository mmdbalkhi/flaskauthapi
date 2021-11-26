#! env/bin/python
""" an api application for secure auth users
"""

import sys

from config import secret_key
from flask import Flask, jsonify, request
from security import check_corrected_v1, password_secure_v1
from sqlite import create_table_v1, read_username_from_sql_v1, write_sql_v1

app = Flask(__name__)
app.secret_key = secret_key


secret_key = app.secret_key
if not secret_key:
    print(
        "ERROR: we Can not Find secret_key. "
        "Please Add secret_key For config.py and Run Again."
        "or You can put your secret key in app.secret_key "
        "(If you put 'flask (__name__)' in a variable named app. Otherwise "
        ",replace the app with your variable name)"
    )
    sys.exit(1)


@app.route("/api/v1/signup", methods=["POST"])
def signup_v1():
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
    if read_username_from_sql_v1(username):
        return jsonify(
            {
                "status": "duplicate",
                "msg": "username already registred",
            }
        )
    if not password_secure_v1(username, password):
        return (
            jsonify(
                {
                    "status": "not secure",
                    "msg": "passoword not secure",
                }
            ),
            406,
        )
    write_sql_v1(username, password)
    return jsonify({"status": "ok", "msg": "user created"})


@app.route("/api/v1/login", methods=["POST"])
def login_v1():
    """get sended datas from user and check"""
    try:
        username = request.form["username"]
        password = request.form["password"]
    except KeyError:
        return (
            jsonify({"status": "error", "msg": "(s) are wrong or incomplete"}),
            405,
        )

    if check_corrected_v1(username, password):
        return jsonify({"status": "ok", "msg": f"accesse Grante for {username}"}), 406

    return jsonify({"status": "faile", "msg": "incorrect username or password"})


if __name__ == "__main__":
    create_table_v1()
    app.run(host="localhost", port=5000, debug=False)
