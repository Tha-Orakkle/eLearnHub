#!/usr/bin/python3
"""handle all RESTful APIs actions for user"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User
import os
upload_folder = os.path.join("web_dynamic", "uploads")



def save_image(user, image, filename):
    """saves/replaces profile picture"""
    file = "profile_pic." + filename.split('.')[1]
    file_path = os.path.join(upload_folder, user.id)
    filename = os.path.join(file_path, file)
    try:
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        else:
            if os.path.exists(filename):
                os.remove(filename)
    except Exception:
        pass
    image.save(filename)
    return os.path.join("uploads", user.id, file)


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retreives a list of  all users object
    """
    usr_list = []
    all_users = storage.all(User).values()
    for user in all_users:
        usr_list.append(user.to_dict())
    return jsonify(usr_list)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Crates a new User"""
    data = request.form
    if not data:
        abort(400)
    if "first_name" not in data or "last_name" not in data:
        abort(400, description="Missing Name")    
    if "password" not in data:
        abort(400, description="Missing password")
    if "email" not in data:
        abort(400, description="Missing email")
    new_user = User(**data)
    if "profile_pic" in request.files:
        image = request.files['profile_pic']
        filename = request.headers.get('X-Original-Filename')
        file_path = save_image(new_user, image, filename)
        new_user.profile_pic = file_path
    new_user.save()
    return jsonify(new_user.to_dict()), 201
    


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Gets the details of a user that matches a user_id"""
    usr = storage.get(User, user_id)
    if usr is None:
        abort(404)
    return jsonify(usr.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User"""
    usr = storage.get(User, user_id)
    if not usr:
        abort(404)
    storage.delete(usr)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """update a user"""
    usr = storage.get(User, user_id)
    if not usr:
        abort(404, description="Invalid user_id")
    if "profile_pic" in request.files and request.files["profile_pic"]:
        image = request.files["profile_pic"]
        filename = request.headers.get('X-Original-Filename')
        file_path = save_image(usr, image, filename)
        usr.profile_pic = file_path
    data = request.form
    if not data:
        abort(400, description="Not a JSON")
    ignore = ['id', 'created', 'updataed_at', 'password']
    for k, v in data.items():
        if k not in ignore and v != "":
            setattr(usr, k, v)
    storage.save()
    return make_response(jsonify(usr.to_dict()), 200)
