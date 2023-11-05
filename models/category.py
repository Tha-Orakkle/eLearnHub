#!/usr/bin/python3
"""Defines the course_category class"""
import models
from models import storage_type
from models.base_model import Base, Basemodel
from sqlalchemy import Column, String


class Category(Basemodel, Base):
    """represents the course category object"""
    if storage_type == "db":
        __tablename__ = "categories"
        name = Column(String(32), nullable=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """Initializes the course category"""
        super().__init__(*args, **kwargs)

    if storage_type != "db":
        @property
        def courses(self):
            """gets all courses associated with a category"""
            course_list = []
            from models.course import Course
            all_course = models.storage.all(Course).values()
            for c in all_course:
                if self.id in c.categories:
                    course_list.append(c)
            return course_list
