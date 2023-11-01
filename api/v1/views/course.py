#!/usr/bin/python3
"""Handles all RESTful API actions for courses"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.course import Course
from models.instructor import Instructor

course_attr = ['instructor_id', 'title', 'requirements',
               'objectives', 'audience']


@app_views.route('/courses', methods=['GET'], strict_slashes=False)
def get_courses():
    """Retrieves a list of all courses"""
    course_list = []
    all_courses = storage.all(Course).values()
    for course in all_courses:
        course_list.append(course.to_dict())
    return jsonify(course_list)

@app_views.route('/courses/<course_id>', methods=['GET'], strict_slashes=False)
def get_course(course_id):
    """Gets a specific course"""
    course = storage.get(Course, course_id)
    if course is None:
        abort(404)
    return jsonify(course.to_dict())

@app_views.route('/courses/<course_id>', methods=['DELETE'], strict_slashes=False)
def delete_course(course_id):
    """Deletes a specific course"""
    course = storage.get(Course, course_id)
    if not course:
        abort(404)
    storage.delete(course)
    storage.save()
    return make_response(jsonify({}), 200)

    
@app_views.route('/courses', methods=['POST'], strict_slashes=False)
def create_course():
    """Creates a Course"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for attr in course_attr:
        if attr not in data:
            abort(400, description="Course {:s} missing".format(attr))
    if storage.get(Instructor, data.get("instructor_id", None)) is None:
        abort(400, description="Invalid instructor_id")
    course = Course(**data)
    course.save()
    return make_response(jsonify(course.to_dict()), 201)
    
@app_views.route('/courses/<course_id>', methods=['PUT'],
                 strict_slashes=False)
def update_course(course_id):
    """updates an existing course"""
    course = storage.get(Course, course_id)
    if not course:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for k, v in data.items():
        if k != "id" and k != "created_at" and k != "updated_at":
            setattr(course, k, v)
    storage.save()
    return make_response(jsonify(course.to_dict()), 200)
