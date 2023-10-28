#!/usr/bin/python3
"""Defines the course_category class"""
# import models
from models import storage_type
from models.base_model import Base, Basemodel
# from models.course import course_category
from sqlalchemy import Column, String
# from sqlalchemy.orm import relationship


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