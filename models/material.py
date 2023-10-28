#!/usr/bin/python3
"""Defines the material class"""

from models import storage_type
from models.base_model import Base, Basemodel
from sqlalchemy import Column, String, ForeignKey


class Material(Basemodel, Base):
    """Represenst the material object"""
    if storage_type == "db":
        __tablename__ = "materials"
        course_id = Column(String(60), ForeignKey('courses.id'), nullable=False)
        description = Column(String(32), nullable=False)
        url = (Column(String(512), nullable=False))
    else:
        course_id = ""
        description = ""
        url = ""
    
    def __init__(self, *args, **kwargs):
        """Initialises the material"""
        super().__init__(*args, **kwargs)