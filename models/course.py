#!/usr/bin/python3
""""Defines the course class"""
import models
from models import storage_type
from models.base_model import Base, Basemodel
from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship

if storage_type == "db":
    course_category = Table('course_category', Base.metadata,
                            Column('course_id', String(60),
                                   ForeignKey('courses.id', onupdate='CASCADE',
                                              ondelete='CASCADE'),
                                   primary_key=True),
                            Column('category_id', String(60),
                                   ForeignKey('categories.id', onupdate='CASCADE',
                                              ondelete='CASCADE'),
                                   primary_key=True)
                            )


class Course(Basemodel, Base):
    """Representation of a course"""
    
    if storage_type == "db":
        __tablename__ = "courses"
        instructor_id = Column(String(60), ForeignKey('instructors.id'), nullable=False)
        title = Column(String(128), nullable=False)
        objectives = Column(String(1024), nullable=False)
        requirements = Column(String(1024), nullable=False)
        audience = Column(String(512), nullable=False)
        lectures = relationship('Lecture', backref='course', cascade='all, delete, delete-orphan')
        materials = relationship('Material', backref='course', cascade='all, delete, delete-orphan')
        categories = relationship('Category', secondary=course_category,
                                  backref="courses", viewonly=False)
    else:
        instructor_id = ""
        title = ""
        objectives = ""
        requirements = ""
        audience = ""
        category_ids = []
        
    def __init__(self, *args, **kwargs):
        """Initializes course"""
        super().__init__(*args, **kwargs)
        
    if storage_type != "db":
        @property
        def lectures(self):
            course_lectures = []
            from models.lecture import Lecture
            all_lectures = models.storage.all(Lecture).values()
            for lecture in all_lectures:
                if self.id == lecture.course_id:
                    course_lectures.append(lecture)
            return course_lectures
        
        @property
        def materials(self):
            course_materials = []
            from models.material import Material
            all_materials = models.storage.all(Material).values()
            for material in all_materials:
                if self.id == material.course_id:
                    course_materials.append(material)
            return course_materials
        
        @property
        def categories(self):
            """Returns all the categories associated with the course"""
            return self.category_ids
           
        @categories.setter
        def categories(self, obj=None):
            """Appends a category to the categories_objs""" 
            from models.category import Category
            if obj and type(obj) is Category and obj not in self.category_ids:
                self.category_ids.append(obj.id)
                self.__dict__["category_ids"] = self.category_ids
            # category_list = []
            # from models.category import Category
            # all_categories = models.storage.all(Category).values()
            # for ca in all_categories:
            #     if self.id == ca.course_id:
            #         category_list.append(ca)
            # return category_list
