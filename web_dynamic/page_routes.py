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

@page_routes.route('/about', methods=['GET'], strict_slashes=False)
def about_page():
    """serves the about page"""
    return render_template('about.html')


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
    if request.method == 'GET':
        usr = storage.get(User, id)
        return render_template('update.html', user=usr)
    elif request.method == 'POST':
        url = "http://127.0.0.1:5000/api/v1/users/{}".format(id)
        data = request.form.to_dict()
        files = {}
        headers = {}
        if "profile_pic" in request.files:
            files['profile_pic'] = request.files.get('profile_pic', None)
            headers["X_-Original-Filename"] = files["profile_pic"].filename
        res = requests.put(url, data=data, files=files, headers=headers)
        if res.status_code != 200:
            return render_template('update.html', status="file not updated")
        usr = storage.get(User, id)
        return render_template('update.html', status="file successfully updated", user=usr)
    
@page_routes.route('/teachers', methods=['GET'], strict_slashes=False)
def teachers():
    """serves the teachers page"""
    id = request.args.get('id', None)
    usr = storage.get(User, id)
    return render_template('teachers.html', user=usr)

@page_routes.route('/courses', methods=['GET'], strict_slashes=False)
def courses():
    """serves the courses page"""
    id = request.args.get(id, None)
    usr = storage.get(User, id)
    st_courses = usr.student_courses
    return render_template('courses.html', user=usr,
                           courses=st_courses)