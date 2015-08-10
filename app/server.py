import json
import random
import string

from app import app
from flask import jsonify, request
from database_helpers import query_db, insert_db
from werkzeug.security import generate_password_hash, check_password_hash


def decorator(func, request, check_token):
    data = request.get_json(force=True)
    try:
        if check_token:
            token = data.get('token', None)
            if token:
                user = query_db('SELECT * FROM Users WHERE token = ?', [token], one=True)
                if user:
                    json, code = func(**data)
                else:
                    json = jsonify(success=False, message='Invalid token')
                    code = 401
            else:
                json = jsonify(success=False, message='Misformatted data.')
                code = 400
        else:
            json, code = func(**data)
    except TypeError:
        json = jsonify(success=False, message='Misformatted data.')
        code = 400
    return json, code


@app.route('/')
def index():
    return "Hello world"


@app.route('/sign_in', methods=['POST'])
def sign_in_helper():
    return decorator(sign_in, request, check_token=False)


def sign_in(email, password):
    data = query_db('SELECT * FROM Users WHERE email = ?', [email], one=True)

    if data and check_password_hash(data["password"], password):
        token = token_creator()
        insert_db('UPDATE Users SET token = ? WHERE email = ?', [token, email])
        return jsonify(
            succes=True,
            message="Welcome",
            data=json.dumps({'token': token}),
            ), 200
    return jsonify(
        success=False,
        message="Username or password invalid"), 401


def token_creator():
    data = query_db('SELECT token FROM Users', one=False)
    while True:
        token = ''.join(random.choice(string.ascii_letters + string.digits)
                        for x in range(32))
        if token not in data:
            return token


@app.route('/sign_up', methods=['POST'])
def sign_up_helper():
    return decorator(sign_up, request, check_token=False)


def sign_up(email, password, firstname, familyname, gender, city, country):
    """
    check if the email exists in the database
    """
    data = query_db('SELECT * FROM Users WHERE email = ?', [email], one=True)
    if data is not None:
        return jsonify(
            success=False,
            message="Email already exists"), 400

    insert_db('INSERT INTO Users  (email, firstname, lastname, gender, city, country, password) \
        VALUES (?, ?, ?, ?, ?, ?, ?)',
              [email, firstname, familyname, gender, city,
               country, generate_password_hash(password)])
    return jsonify(
            success=True,
            message="Account created successfully"), 200


@app.route("/sign_out", methods=['PUT'])
def sign_out_helper():
    return decorator(sign_out, request, check_token=True)


def sign_out(token):
    query_db('UPDATE Users SET token = null WHERE token = ?', [token], one=True)
    return jsonify(
        success=True,
        message="You are now signed out"), 200


@app.route("/change_password", methods=['PUT'])
def change_password_helper():
    return decorator(change_password, request, check_token=True)


def change_password(token, old_password, new_password):
    data = query_db('SELECT * FROM Users WHERE token = ?', [token], one=True)
    if not check_password_hash(data["password"], password):
        return jsonify(
            success=False,
            message="Incorect password"), 400

    insert_db('UPDATE Users WHERE id=? SET password = ?', [data["id"],
                                                           new_password])
    return jsonify(
            success=True,
            message="Password changed successfully"), 200


@app.route("/profile", methods=['GET'])
def get_user_data_by_token_helper():
    return decorator(get_user_data_by_token, request, check_token=True)


def get_user_data_by_token(token):
    data = query_db('SELECT * FROM Users WHERE token = ?', [token], one=True)
    return jsonify(
        success=True,
        email=data["email"],
        firstname=data["firstname"],
        lastname=data["lastname"],
        gender=data["gender"],
        city=data["city"],
        country=data["country"])


@app.route("/user", methods=['GET'])
def get_user_data_by_email_helper():
    return decorator(get_user_data_by_email, request, check_token=True)


def get_user_data_by_email(token, email):
    data = query_db('SELECT * FROM Users WHERE email = ? AND token = ?',
                    [email, token], one=True)
    return jsonify(
        success=True,
        email=data["email"],
        firstname=data["firstname"],
        lastname=data["lastname"],
        gender=data["gender"],
        city=data["city"],
        country=data["country"]), 200


@app.route("/profile_messages", methods=['GET'])
def get_user_messages_by_token_helper():
    return decorator(get_user_messages_by_token, request, check_token=True)


def get_user_messages_by_token(token):
    data = query_db('SELECT * FROM Users WHERE token = ?', [token], one=True)
    data_messages = query_db('SELECT * FROM Messages WHERE sender = ?', [data["id"]], one=False)
    return jsonify(
        data=json.dumps(data_messages),
        )


@app.route("/user_profile", methods=['GET'])
def get_user_messages_by_email_helper():
    return decorator(get_user_messages_by_email, request, check_token=True)


def get_user_messages_by_email(token, email):
    data = query_db('SELECT * FROM Users WHERE email= ?', [email], one=True)
    data_messages = query_db('SELECT * FROM Messages WHERE sender = ?', [data["id"]], one=False)
    return jsonify(
        data=json.dumps(data_messages),
        )


@app.route("/message", methods=['GET', 'POST'])
def post_message_helper():
    return decorator(post_message, request, check_token=True)


def post_message(token, message, email):
    data = query_db('SELECT * FROM Users WHERE email= ?', [email], one=True)
    my_data = query_db('SELECT * FROM Users WHERE token= ?', [token], one=True)
    if data is None:
        return jsonify(
            success=False,
            message="Recipient does not exist"), 400
    insert_db('INSERT INTO Messages (receiver, sender, message) \
        VALUES (?, ?, ?, ?)', [data["id"], my_data["id"], message])
    return jsonify(
        success=True,
        message="Message posted successfully"), 200
