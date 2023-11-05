#!/usr/bin/python3
"""test material fo rexpected behaviour"""

import inspect
import models
from models.material import Material
import pycodestyle
import unittest
module_doc = models.material.__doc__


class TestMaterialDocs(unittest.TestCase):
    """test to check the documentation and style of Material class"""

    @classmethod
    def setUpClass(self):
        """set up class for docstring tests"""
        self.material_funcs = inspect.getmembers(Material, inspect.isfunction)

    def test_pycodestyle_conformity(self):
        """Test that models/material.py conforms with pycodestyle"""
        paths = ['models/material.py', 'tests/test_models/test_material.py']
        for path in paths:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test that the module has a docstring"""
        self.assertIsNot(module_doc, None,
                         "material.py needs a docstring")
        self.assertTrue(len(module_doc) > 1,
                        "material.py needs a docstring")

    def test_class_docstring(self):
        """Tests that the class hasd a docstring"""
        self.assertIsNot(Material.__doc__, None,
                         "Material class needs a docstring")
        self.assertTrue(len(Material.__doc__) > 1,
                        "Material class needs a docstring")

    def test_func_docstrings(self):
        """Tests for the presence of docstrings in all Material methods"""
        for func in self.material_funcs:
            with self.subTest(func=func):
                self.assertIsNot(
                    func[1].__doc__, None,
                    "{:s} methods needs a docstring".format(func[0])
                    )
                self.assertTrue(
                    len(func[1].__doc__) > 1,
                    "{:s} method need a docstring".format(func[0])
                    )
