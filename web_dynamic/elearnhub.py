#!/usr/bin/python3
"""main application file"""
import base64
import bcrypt
import requests
from flask import abort, Flask, render_template, request, jsonify
from models import storage
from models.user import User
from web_dynamic.page_routes import page_routes


app = Flask(__name__)
app.register_blueprint(page_routes)

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
    
@app.route('/home', methods=['GET'], strict_slashes=False)
def home():
    """serves the landing page"""
    return render_template('index.html')

@app.route('/sign_up', methods=['POST'], strict_slashes=False)
def sign_up():
    """Registers a  new user"""
    url = "http://127.0.0.1:5000/api/v1/users"
    data = request.form
    files = {}
    headers = {}
    if "email" not in data:
        abort(400, description="Missing email")
    all_usrs = storage.all(User).values()
    for usr in all_usrs:
        if data["email"] == usr.email:
            return render_template('register.html', error="User with the email already exists")
    req_files = request.files
    if "profile_pic" in req_files and req_files["profile_pic"].filename != "":
        image = req_files["profile_pic"]
        files["profile_pic"] = image
        headers['X-Original-Filename'] = image.filename
    data_copy = data.to_dict(flat=True)
    response = requests.post(url, data=data_copy, files=files, headers=headers)
    if response.status_code != 201:
        return render_template('register.html', error="error occured")
    id  = response.json().get("id")
    storage.save()
    usr = storage.get(User, id)
    return render_template('home.html', user=usr)
    
@app.route('/login', methods=['POST'], strict_slashes=False)
def login():
    """log in as a user"""
    data = request.form
    if not data:
        return render_template('login.html', error="Enter login details")
    if "email" not in data:
        return render_template('login.html', error="Invalid email")
    if "password" not in data:
        return render_template('login.html', error="Invalid password")
    email = data["email"]
    password = data["password"]
    usr = decrypt_password(email, password)
    if usr is None:
        return render_template('login.html', error="email/password is invalid")
    return render_template('home.html', user=usr)
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5001", debug=True)