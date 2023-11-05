#!/usr/bin/python3
"""test instructor fo rexpected behaviour"""

import inspect
import models
from models.instructor import Instructor
import pycodestyle
import unittest
module_doc = models.instructor.__doc__


class TestInstructorDocs(unittest.TestCase):
    """test to check the documentation and style of Instructor class"""

    @classmethod
    def setUpClass(self):
        """set up class for docstring tests"""
        self.instructor_funcs = inspect.getmembers(Instructor,
                                                   inspect.isfunction)

    def test_pycodestyle_conformity(self):
        """Test that models/instructor.py conforms with pycodestyle"""
        paths = ['models/instructor.py',
                 'tests/test_models/test_instructor.py']
        for path in paths:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test that the module has a docstring"""
        self.assertIsNot(module_doc, None,
                         "instructor.py needs a docstring")
        self.assertTrue(len(module_doc) > 1,
                        "instructor.py needs a docstring")

    def test_class_docstring(self):
        """Tests that the class hasd a docstring"""
        self.assertIsNot(Instructor.__doc__, None,
                         "Instructor class needs a docstring")
        self.assertTrue(len(Instructor.__doc__) > 1,
                        "Instructor class needs a docstring")

    def test_func_docstrings(self):
        """Tests for the presence of docstrings in all Instructor methods"""
        for func in self.instructor_funcs:
            with self.subTest(func=func):
                self.assertIsNot(
                    func[1].__doc__, None,
                    "{:s} methods needs a docstring".format(func[0])
                    )
                self.assertTrue(
                    len(func[1].__doc__) > 1,
                    "{:s} method need a docstring".format(func[0])
                    )
