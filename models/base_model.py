#!/usr/bin/python3
"""
Defines the base_model class
"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from models import storage_type
import uuid

format = "%Y-%m-%d %H:%M:%S.%f"
if storage_type == "db":
    Base = declarative_base()
else:
    Base = object


class Basemodel():
    """Basemodel class that will be inherited by other class"""
    if storage_type == "db":
        id = Column(String(60), unique=True, nullable=False, primary_key=True)
        created_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow())
        updated_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initializes the basemodel"""
        if kwargs:
            if kwargs.get('id', None) is None:
                self.id = str(uuid.uuid4())
            for k, v in kwargs.items():
                if k != "__class__":
                    setattr(self, k, v)
            if kwargs.get('created_at', None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"],
                                                    format)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get('updated_at', None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"],
                                                    format)
            else:
                self.updated_at = datetime.utcnow()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """String representation of the Basemodel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def to_dict(self):
        """converts the object to a dictionary and returns it"""
        temp = self.id
        new_dict = self.__dict__.copy()
        new_dict['__class__'] = self.__class__.__name__
        if "created_at" in new_dict:
            new_dict["created_at"] = str(new_dict["created_at"])
        if "updated_at" in new_dict:
            new_dict["updated_at"] = str(new_dict["updated_at"])
        if "_sa_instance_state" in new_dict:
            del new_dict['_sa_instance_state']
        if storage_type == "db":
            if "password" in new_dict:
                del new_dict["password"]
            if "password_salt" in new_dict:
                del new_dict["password_salt"]
        return new_dict

    def save(self):
        """saves new object and updates attr 'updated_at'"""
        self.updated_at = datetime.utcnow()
        from models import storage
        storage.new(self)
        storage.save()
