#!/usr/bin/python3
"""handle all RESTful APIs actions for user"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User
import os
upload_folder = "uploads"


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
    if "image" in request.files:
        image = request.files['image']
        profile_path = os.path.join(upload_folder, data['email'])
        if not os.path.exists(profile_path):
            os.makedirs(profile_path)
        filename = os.path.join(profile_path, image.filename)
        image.save(filename)
        data = data.to_dict()
        data['profile_pic'] = filename
    new_user = User(**data)
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
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for k, v in data.items():
        if k != "id" and k != "created_at" and k != "updated_at":
            setattr(usr, k, v)
    storage.save()
    return make_response(jsonify(usr.to_dict()), 200)
