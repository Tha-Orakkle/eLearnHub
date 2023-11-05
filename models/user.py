#!/usr/bin/python3
"""
Defines the user class
"""
import base64
import bcrypt
import models
from models import storage_type
from models.base_model import Base, Basemodel
from models.instructor import Instructor
from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import relationship

if storage_type == "db":
    course_enroll = Table('couse_enroll', Base.metadata,
                          Column('user_id', String(60),
                                 ForeignKey('users.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True),
                          Column('course_id', String(60),
                                 ForeignKey('courses.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True)
                          )


class User(Basemodel, Base):
    """Representation of a user"""
    if storage_type == "db":
        __tablename__ = "users"
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        password_salt = Column(String(60), nullable=False)
        first_name = Column(String(32), nullable=False)
        last_name = Column(String(32), nullable=False)
        telephone = Column(String(32), nullable=True)
        instructor = relationship('Instructor', backref='user', uselist=False,
                                  cascade="all, delete-orphan")
        student_courses = relationship('Course', secondary=course_enroll,
                                       backref='students', viewonly=False)
    else:
        email = ""
        password = None
        pasword_salt = ""
        first_name = ""
        last_name = ""
        telephone = ""
        instructor = None
        student_courses_ids = []

    def __init__(self, *args, **kwargs):
        """initializes user"""
        if kwargs and kwargs['password']:
            pwd = kwargs['password']
            salt = bcrypt.gensalt()
            self.password_salt = base64.b64encode(salt).decode('utf-8')
            pwd = bcrypt.hashpw(pwd.encode('utf-8'), salt)
            self.password = base64.b64encode(pwd).decode('utf-8')
            del kwargs['password']
        super().__init__(*args, **kwargs)

    if storage_type != "db":
        @property
        def instructor(self):
            """getter attribute that returns an the obj of the instructor"""
            all_instructors = models.storage.all(Instructor).values()
            for instructor in all_instructors:
                if instructor.user_id == self.id:
                    return instructor

        @property
        def student_courses(self):
            """gets all the courses that a student is subscribed to"""
            return self.student_courses_ids

        @student_courses.setter
        def student_courses(self, obj=None):
            """adds to a course to the list of courses offered by a student"""
            from models.course import Course
            sc_ids = self.student_courses_ids
            if obj and type(obj) is Course and obj.id not in sc_ids:
                self.student_courses_ids.append(obj.id)
                self.__dict__["student_courses_ids"] = self.student_courses_ids
