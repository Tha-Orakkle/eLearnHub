#!/usr/bin/python3
"""Handles all RESTfl API actions for instructor"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response
from models import storage
from models.user import User
from models.instructor import Instructor


def create_instructor_user_details(user, instructor):
    """returns a dictionary that contains a the
    instructor's user info and the instructor info"""
    user_d = user.to_dict()
    instructor_d = instructor.to_dict()
    user_d['instructor_info'] = instructor_d
    return user_d


@app_views.route('/instructors', methods=['GET'], strict_slashes=False)
def get_instructors():
    "Retrieves a list of all instructors on the platform"
    instructor_list = []
    all_instructors = storage.all(Instructor).values()
    for instructor in all_instructors:
        instructor_list.append(instructor.to_dict())
    return jsonify(instructor_list)


@app_views.route('/instructors/<instructor_id>', methods=['GET'],
                 strict_slashes=False)
def get_instructor(instructor_id):
    """Gets a specific instructor"""
    instructor = storage.get(Instructor, instructor_id)
    if not instructor:
        abort(404)
    return jsonify(instructor.to_dict())


@app_views.route('/instructors/<instructor_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_instructor(instructor_id):
    """deletes an instructor"""
    instructor = storage.get(Instructor, instructor_id)
    if not instructor:
        abort(404)
    storage.delete(instructor)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users/<user_id>/instructor', methods=['POST'],
                 strict_slashes=False)
def create_instructor(user_id):
    """Creates instructor and links to a user"""
    usr = storage.get(User, user_id)
    if not usr:
        abort(404)
    instructor = Instructor(**{"user_id": usr.id})
    usr.is_instructor = True
    instructor.save()
    usr.save()
    user_instructor = create_instructor_user_details(usr, instructor)
    return make_response(jsonify(user_instructor))
