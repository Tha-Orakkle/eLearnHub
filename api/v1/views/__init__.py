#!/usr/bin/python3
"""Blueprint for APIS"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.user import *
from api.v1.views.course import *
from api.v1.views.instructors import *
