#!/usr/bin/python3
"""handle all RESTful APIs actions for user"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


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
