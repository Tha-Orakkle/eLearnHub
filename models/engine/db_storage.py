#!/usr/bin/python3
"""Database Storage Engine"""
from models.base_model import Base
from models.category import Category
from models.course import Course
from models.instructor import Instructor
from models.lecture import Lecture
from models.material import Material
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import environ


class DBStorage:
    """creates a database"""
    
    __engine = None
    __session = None
    
    def __init__(self):
        """Instantiate the DBStorage object"""
        MYSQL_USER = environ.get('ELH_MYSQL_USER')
        MYSQL_PWD = environ.get('ELH_MYSQL_PWD')
        MYSQL_HOST = environ.get('ELH_MYSQL_HOST')
        MYSQL_DB = environ.get('ELH_MYSQL_DB')
        
        # self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
        #     MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_DB
        # ))
        self.__engine = create_engine("sqlite:///file.db")
        
    def all(self, cls=None):
        """Returns all objects or the object of a specific class"""
        all_objs = {}
        if cls:
            if type(cls) == str:
                cls = eval(cls)
            cls_objs = self.__session.query(cls).all()
            for obj in cls_objs:
                key = type(obj).__name__ + '.' + obj.id
                all_objs[key] = obj
        else:
            classes = [User, Course, Category, Instructor, Lecture, Material]
            for clss in classes:
                cls_objs = self.__session.query(clss).all()
                for obj in cls_objs:
                    key = type(obj).__name__ + '.' + obj.id
                    all_objs[key] = obj
        return all_objs
    
    def new(self, obj):
        """adds a new object to the database session"""
        self.__session.add(obj)
    
    def save(self):
        """commits all changes to the database session"""
        self.__session.commit()
        
    def delete(self, obj=None):
        """deletes an obj"""
        if obj:
            self.__session.delete(obj)
            
    def get(self, cls, id):
        """gets an obj based on class name and id"""
        return self.__session.query(cls).filter(cls.id == id).first()
        
    def reload(self):
        """reloads data from database"""
        Base.metadata.create_all(self.__engine)
        sesh = sessionmaker(bind=self.__engine, expire_on_commit=True)
        Session = scoped_session(sesh)
        self.__session = Session()
        
    def close(self):
        """removes the private database session"""
        self.__session.remove()