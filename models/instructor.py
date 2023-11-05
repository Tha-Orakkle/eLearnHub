#!/usr/bin/python3
"""
Defines the Instructor class
"""
import models
from models import storage_type
from models.base_model import Base, Basemodel
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Instructor(Basemodel, Base):
    """Representation of an instructor"""
    if storage_type == "db":
        __tablename__ = "instructors"
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        courses = relationship('Course', backref='instructor',
                               cascade='all, delete, delete-orphan')
    else:
        user_id = ""
        courses = []
        user = None

    def __init__(self, *args, **kwargs):
        """initializes the instructor"""
        super().__init__(*args, **kwargs)

    if storage_type != "db":
        @property
        def courses(self):
            instructor_courses = []
            from models.course import Course
            all_courses = models.storage.all(Course).values()
            for course in all_courses:
                if self.id == course.instructor_id:
                    instructor_courses.append(course)
            return instructor_courses

        @property
        def user(self):
            """getter attribute that returns the user object"""
            from models.user import User
            all_usrs = models.storage.all(User).values()
            for usr in all_usrs:
                usr_instructor = usr.instructor
                if self.id == usr_instructor.id:
                    return usr
