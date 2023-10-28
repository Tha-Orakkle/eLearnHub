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
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship


class User(Basemodel, Base):
    """Representation of a user"""
    if storage_type == "db":
        __tablename__ = "users"
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        password_salt = Column(String(32), nullable=False)
        first_name = Column(String(32), nullable=False)
        last_name = Column(String(32), nullable=False)
        telephone = Column(String(32), nullable=True)
        instructor = relationship('Instructor', backref='user', uselist=False, cascade="all, delete-orphan")
    else:
        email = ""
        password = None
        pasword_salt = ""
        first_name = ""
        last_name = ""
        telephone = ""
        instructor = None
        
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
                
        
    # @property
    # def password(self):
    #     """gets the password"""
    #     return self.__password
    
    # @password.setter
    # def password(self, value):
    #     """sets the password"""
    #     salt = bcrypt.gensalt()
    #     self.password_salt = base64.b64encode(salt).decode('utf-8')
    #     pwd = bcrypt.hashpw(value.encode('utf-8'), salt)
    #     self.password = base64.b64encode(pwd).decode('utf-8')
        
    if storage_type != "db":
        @property
        def instructor(self):
            """getter attribute that returns an the obj of the instructor"""
            all_instructors = models.storage.all(Instructor).values()
            for instructor in all_instructors:
                if instructor.user_id == self.id:
                    return instructor