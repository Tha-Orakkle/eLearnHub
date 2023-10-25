#!/usr/bin/python3
"""
Defines the user class
"""
import base64
import bcrypt
from models import storage_type
from models.base_model import Base, Basemodel
from sqlalchemy import Column, String, Boolean


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

        instructor = Column(Boolean, nullable=False, default=False)
    else:
        email = ""
        password = ""
        pasword_salt = ""
        first_name = ""
        last_name = ""
        telephone = ""
        
        instructor = False
        
    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs) 
        
    @property
    def password(self):
        """gets the password"""
        return self.__password
    
    @password.setter
    def password(self, value):
        """sets the password"""
        salt = bcrypt.gensalt()
        self.password_salt = base64.b64encode(salt).decode('utf-8')
        pwd = bcrypt.hashpw(value.encode('utf-8'), salt)
        self.__password = base64.b64encode(pwd).decode('utf-8')