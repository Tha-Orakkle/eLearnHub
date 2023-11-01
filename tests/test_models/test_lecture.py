#!/usr/bin/python3
"""test lecture fo rexpected behaviour"""

import inspect
import models
from models.lecture import Lecture
import pycodestyle
import unittest
module_doc = models.lecture.__doc__


class TestLectureDocs(unittest.TestCase):
    """test to check the documentation and style of Lecture class"""

    @classmethod
    def setUpClass(self):
        """set up class for docstring tests"""
        self.lecture_funcs = inspect.getmembers(Lecture, inspect.isfunction)

    def test_pycodestyle_conformity(self):
        """Test that models/lecture.py conforms with pycodestyle"""
        paths = ['models/lecture.py', 'tests/test_models/test_lecture.py']
        for path in paths:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test that the module has a docstring"""
        self.assertIsNot(module_doc, None,
                         "lecture.py needs a docstring")
        self.assertTrue(len(module_doc) > 1,
                        "lecture.py needs a docstring")

    def test_class_docstring(self):
        """Tests that the class hasd a docstring"""
        self.assertIsNot(Lecture.__doc__, None,
                         "Lecture class needs a docstring")
        self.assertTrue(len(Lecture.__doc__) > 1,
                        "Lecture class needs a docstring")

    def test_func_docstrings(self):
        """Tests for the presence of docstrings in all Lecture methods"""
        for func in self.lecture_funcs:
            with self.subTest(func=func):
                self.assertIsNot(
                    func[1].__doc__, None,
                    "{:s} methods needs a docstring".format(func[0])
                    )
                self.assertTrue(
                    len(func[1].__doc__) > 1,
                    "{:s} method need a docstring".format(func[0])
                    )
