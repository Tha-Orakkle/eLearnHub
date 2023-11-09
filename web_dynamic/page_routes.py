#!/usr/bin/python3
"""Blueprint for the main application.
Contains all page routes"""
from flask import Blueprint, render_template, request
from models import storage
from models.user import User
import requests

page_routes = Blueprint('page_routes', __name__, url_prefix="/",
                        template_folder='templates')

@page_routes.route('/elearn', methods=['GET'], strict_slashes=False)
def elearn():
    """ElearnHub Home"""
    return render_template('home.html')


@page_routes.route('/register', methods=['GET'], strict_slashes=False)
def register():
    """serves the register page"""
    return render_template('register.html')

@page_routes.route('/sign_in', methods=['GET'], strict_slashes=False)
def sign_in():
    """serves the login page"""
    return render_template('login.html')

@page_routes.route('/profile/<id>', methods=['GET'], strict_slashes=False)
def profile(id):
    """serves the profile page"""
    usr = storage.get(User, id)
    return render_template('profile.html', user=usr)

@page_routes.route('/profile/<id>/update', methods=['GET', 'POST'], strict_slashes=False)
def profile_update(id):
    """serves the update page"""
    usr = storage.get(User, id)
    if request.method == 'GET':
        return render_template('update.html', user=usr)
    elif request.method == 'POST':
        url = "http://127.0.0.1:5000/api/v1/users/{}".format(usr.id)
        data = request.form.to_dict()
        files = {'profile_pic': request.files.get('profile_pic', None)}
        res = requests.put(url, data=data, files=files)
        # =========In progesss =================

@page_routes.route('/courses', methods=['GET'], strict_slashes=False)
def courses():
    """serves the courses page"""
    return render_template('courses.html')