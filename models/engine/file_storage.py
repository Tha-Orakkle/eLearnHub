#!/usr/bin/python3
"""File Storage Engine"""
import json
from models.category import Category
from models.course import Course
from models.instructor import Instructor
from models.lecture import Lecture
from models.material import Material
from models.user import User

classes = {"Category": Category, "Course": Course, "Instructor": Instructor,
           "Lecture": Lecture, "Material": Material, "User": User}


class FileStorage:
    """creates file storage by serializing and deserializing instancd"""

    # dictionary to store all objects by the class and id
    __objects = {}

    # JSON file location
    __file_path = "file.json"

    def all(self, cls=None):
        """returns all objects or the objects of a specific class"""
        if cls is not None:
            new_obj_list = {}
            for k, v in self.__objects.items():
                if cls == v.__class__ or cls == v.__class__.__name__:
                    new_obj_list[k] = v
            return new_obj_list
        return self.__objects

    def new(self, obj):
        """adds new object to __objects with the key <class>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            self.__objects[key] = obj

    def save(self):
        """serializes __object to a json file"""
        json_dict = {}
        for k, v in self.__objects.items():
            json_dict[k] = v.to_dict()
        with open(self.__file_path, "w") as f:
            json.dump(json_dict, f)

    def delete(self, obj):
        """deletes a item from the __object"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def get(self, cls, id):
        """gets an object based on class name and id"""
        if cls not in classes.values():
            return None
        from models import storage
        all_clss = storage.all(cls)
        for v in all_clss.values():
            if (v.id == id):
                return v
        return None

    def reload(self):
        """deserializes JSOn file to __objects"""
        try:
            with open(self.__file_path, "r") as f:
                data = json.load(f)
                for k, v in data.items():
                    self.__objects[k] = classes[v["__class__"]](**v)
        except OSError:
            pass

    def close(self):
        """calls the reload method"""
        self.reload()
