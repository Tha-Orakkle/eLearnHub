#!/usr/bin/python3
import base64
import bcrypt
from flask import abort, Flask, jsonify, render_template, request
from models import storage
from models.user import User
import requests

app = Flask(__name__)


def decrypt_password(email, password):
    """Decrypts password to find matching user"""
    all_usrs = storage.all(User).values()
    for usr in all_usrs:
        if email == usr.email:
            usr_hpwd = base64.b64decode(usr.password)
            usr_pwd_salt = base64.b64decode(usr.password_salt)
            hash_entered_pwd = bcrypt.hashpw(password.encode('utf-8'),
                                             usr_pwd_salt)
            if usr_hpwd == hash_entered_pwd:
                return usr

    return None


@app.teardown_appcontext
def close_db(error):
    """removes current session"""
    storage.close()


@app.route('/elearn', methods=['GET'], strict_slashes=False)
def elearn():
    """ElearnHub Home"""
    return render_template('home.html')


@app.route('/register', methods=['GET'], strict_slashes=False)
def register():
    """serves the register page"""
    return render_template('register.html')

@app.route('/sign_in', methods=['GET'], strict_slashes=False)
def sign_in():
    """serves the login page"""
    return render_template('login.html')

@app.route('/sign_up', methods=['POST'], strict_slashes=False)
def sign_up():
    """Registers a  new user"""
    app.config['UPLOAD_FOLDER'] = "uploads"
    url = "http://127.0.0.1:5000/api/v1/users"
    files = {}
    data = request.form
    if "email" not in data:
        abort(400, description="Missing email")
    all_usrs = storage.all(User).values()
    for usr in all_usrs:
        if data["email"] == usr.email:
            abort(400, description="User already exists")
     
    if "profile_pic" in request.files:
        image = request.files['profile_pic']
        if image.filename == '':
            abort(400, description="No file Selected")
        files['image'] = (image.filename, image.stream)
    
    data_copy = data.to_dict(flat=True)
    response = requests.post(url, data=data_copy, files=files)
    if response.status_code != 201:
        abort(400, description="User not created")
    usr = storage.get(User, response.json()['id'])
    return render_template('home.html',
                           user=usr)
    
@app.route('/login', methods=['POST'], strict_slashes=False)
def login():
    """log in as a user"""
    data = request.form
    if not data:
        abort(400)
    if "email" not in data:
        abort(400, description="Missing email")
    if "password" not in data:
        abort(400, description="Missing password")
    email = data["email"]
    password = data["password"]
    usr = decrypt_password(email, password)
    if usr is None:
        abort(400, description="User does not exit")
    return render_template('home.html', user=usr)
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5001", debug=True)