#!/usr/bin/python3
"""Handles user creation and authentication"""
from api.v1.views import app_views
import base64
import bcrypt
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User

def decrypt_password(email, password):
    """Decrypts password to find matching user"""
    all_usrs = storage.all(User).values()
    for usr in all_usrs:
        if email == usr.email:
            usr_hpwd = base64.b64decode(usr.password)
            usr_pwd_salt = base64.b64decode(usr.password_salt)
            hash_entered_pwd = bcrypt.hashpw(password.encode('utf-8'), usr_pwd_salt)
            if usr_hpwd == hash_entered_pwd:
                return usr
    return None
    

@app_views.route('/sign_up', methods=['POST'], strict_slashes=False)
def sign_up():
    """Crates a new User"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if "email" not in data:
        abort(400, description="Missing email")
    if "password" not in data:
        abort(400, description="Missing password")
    if "first_name" not in data or "last_name" not in data:
        abort(400, description="Missing Name")
    
    new_user = User(**data)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)

@app_views.route('/login', methods=['POST'], strict_slashes=False)
def login():
    """Returns the user"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if "email" not in data:
        abort(400, description="Missing email")
    if "password" not in data:
        abort(400, description="Missing password")
    email = data["email"]
    password = data["password"]
    usr = decrypt_password(email, password)
    if usr is None:
        abort(400, description="User does not exit")
    return jsonify(usr.to_dict())