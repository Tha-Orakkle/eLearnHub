#!/usr/bin/python3
"""test user fo rexpected behaviour"""

import inspect
import models
from models.category import Category
import pycodestyle
import unittest
module_doc = models.category.__doc__


class TestUserDocs(unittest.TestCase):
    """test to check the documentation and style of Category class"""

    @classmethod
    def setUpClass(self):
        """set up class for docstring tests"""
        self.category_funcs = inspect.getmembers(Category, inspect.isfunction)

    def test_pycodestyle_conformity(self):
        """Test that models/user.py conforms with pycodestyle"""
        paths = ['models/category.py', 'tests/test_models/test_category.py']
        for path in paths:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test that the module has a docstring"""
        self.assertIsNot(module_doc, None,
                         "category.py needs a docstring")
        self.assertTrue(len(module_doc) > 1,
                        "category.py needs a docstring")

    def test_class_docstring(self):
        """Tests that the class hasd a docstring"""
        self.assertIsNot(Category.__doc__, None,
                         "Category class needs a docstring")
        self.assertTrue(len(Category.__doc__) > 1,
                        "Category class needs a docstring")

    def test_func_docstrings(self):
        """Tests for the presence of docstrings in all Category methods"""
        for func in self.category_funcs:
            with self.subTest(func=func):
                self.assertIsNot(
                    func[1].__doc__, None,
                    "{:s} methods needs a docstring".format(func[0])
                    )
                self.assertTrue(
                    len(func[1].__doc__) > 1,
                    "{:s} method need a docstring".format(func[0])
                    )
