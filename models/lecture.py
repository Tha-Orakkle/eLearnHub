#!/usr/bin/python3
"""Defines the lecture class"""
import models
from models import storage_type
from models.base_model import Base, Basemodel
from sqlalchemy import Column, String, ForeignKey, Integer


class Lecture(Basemodel, Base):
    """Represents the lecture object"""
    if storage_type == "db":
        __tablename__ = "lectures"
        course_id = Column(String(60), ForeignKey('courses.id'),
                           nullable=False)
        description = Column(String(32), nullable=False)
        url = Column(String(1024), nullable=False)
    else:
        course_id = ""
        description = ""
        url = ""

    def __init__(self, *args, **kwargs):
        """initializes the lecture"""
        super().__init__(*args, **kwargs)

    if storage_type != "db":
        @property
        def course(self):
            """gets the course the lecture belongs to"""
            from models.course import Course
            return models.storage.get(Course, self.course_id)
