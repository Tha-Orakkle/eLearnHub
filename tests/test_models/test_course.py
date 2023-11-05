#!/usr/bin/python3
"""test course fo rexpected behaviour"""

import inspect
import models
from models.base_model import Basemodel
from models.course import Course
import pycodestyle
import unittest
module_doc = models.course.__doc__


class TestCourseDocs(unittest.TestCase):
    """test to check the documentation and style of Course class"""

    @classmethod
    def setUpClass(self):
        """set up class for docstring tests"""
        self.course_funcs = inspect.getmembers(Course, inspect.isfunction)

    def test_pycodestyle_conformity(self):
        """Test that models/course.py conforms with pycodestyle"""
        paths = ['models/course.py', 'tests/test_models/test_course.py']
        for path in paths:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test that the module has a docstring"""
        self.assertIsNot(module_doc, None,
                         "course.py needs a docstring")
        self.assertTrue(len(module_doc) > 1,
                        "course.py needs a docstring")

    def test_class_docstring(self):
        """Tests that the class hasd a docstring"""
        self.assertIsNot(Course.__doc__, None,
                         "Course class needs a docstring")
        self.assertTrue(len(Course.__doc__) > 1,
                        "Course class needs a docstring")

    def test_func_docstrings(self):
        """Tests for the presence of docstrings in all Course methods"""
        for func in self.course_funcs:
            with self.subTest(func=func):
                self.assertIsNot(
                    func[1].__doc__, None,
                    "{:s} methods needs a docstring".format(func[0])
                    )
                self.assertTrue(
                    len(func[1].__doc__) > 1,
                    "{:s} method need a docstring".format(func[0])
                    )


class TestCourse(unittest.TestCase):
    """Tests the Course class"""
    def test_is_childclass(self):
        """tests that course is a child clss of Basemodel"""
        course = Course()
        self.assertIsInstance(course, Basemodel)
        self.assertTrue(hasattr(course, "id"))
        self.assertTrue(hasattr(course, "created_at"))
        self.assertTrue(hasattr(course, "updated_at"))

    def test_instructor_id_attr(self):
        """tests that the course instance has an instructor_id"""
        course = Course()
        self.assertTrue(hasattr(course, "instructor_id"))
        if models.storage_type == "db":
            self.assertEqual(course.instructor_id, None)
        else:
            self.assertEqual(course.instructor_id, "")

    def test_title_attr(self):
        """tests that the course instance has a title attibute"""
        course = Course()
        self.assertTrue(hasattr(course, "title"))
        if models.storage_type == "db":
            self.assertEqual(course.title, None)
        else:
            self.assertEqual(course.title, "")

    def test_objectives_attr(self):
        """tests that the course instance has a objectives attibute"""
        course = Course()
        self.assertTrue(hasattr(course, "objectives"))
        if models.storage_type == "db":
            self.assertEqual(course.objectives, None)
        else:
            self.assertEqual(course.objectives, "")

    def test_requirements_attr(self):
        """tests that the course instance has a requirements attibute"""
        course = Course()
        self.assertTrue(hasattr(course, "requirements"))
        if models.storage_type == "db":
            self.assertEqual(course.requirements, None)
        else:
            self.assertEqual(course.requirements, "")

    def test_audience_attr(self):
        """tests that the course instance has a audience attibute"""
        course = Course()
        self.assertTrue(hasattr(course, "audience"))
        if models.storage_type == "db":
            self.assertEqual(course.audience, None)
        else:
            self.assertEqual(course.audience, "")

    @unittest.skipIf(models.storage_type == "db",
                     "not testing for File storage")
    def test_category_ids_attr(self):
        """tests that the course instance has a category_ids attribute"""
        course = Course()
        self.assertTrue(hasattr(course, "category_ids"))
        self.assertEqual(type(course.category_ids), list)
        self.assertEqual(len(course.category_ids), 0)

    def test_to_dict_creates_dict(self):
        """Tests that the to_dict method creates a dictionary"""
        course = Course()
        course_d = course.to_dict()
        self.assertEqual(type(course_d), dict)
        self.assertFalse("_sa_instance_state" in course_d)
        for attr in course.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in course_d)
        self.assertTrue("__class__" in course_d)

    def test_to_dict_values(self):
        """tests that the values returned by tthe to_dict method are valid"""
        format = "%Y-%m-%d %H:%M:%S.%f"
        course = Course()
        course_d = course.to_dict()
        self.assertEqual(course_d["__class__"], "Course")
        self.assertEqual(type(course_d["created_at"]), str)
        self.assertEqual(type(course_d["updated_at"]), str)
        self.assertEqual(course_d["created_at"],
                         course.created_at.strftime(format))
        self.assertEqual(course_d["updated_at"],
                         course.updated_at.strftime(format))
