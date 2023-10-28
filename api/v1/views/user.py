#!/usr/bin/python3
"""Objects that handle all RESTful APIs actions for user"""
from api.v1.views import app_views
from flask import jsonify
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
    
    