#!/usr/bin/python3
"""
This script includes tests for file_storage.py in the models/engine directory.

Test classes included:
    TestFileStorageCreation
    TestFileStorageFunctions
"""
import os
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorageCreation(unittest.TestCase):
    """Tests to check the creation of FileStorage instances."""

    def test_creation_without_arguments(self):
        self.assertIsInstance(FileStorage(), FileStorage)

    def test_creation_with_argument_raises_error(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_file_path_private_and_string(self):
        self.assertIsInstance(FileStorage._FileStorage__file_path, str)

    def test_objects_private_and_dictionary(self):
        self.assertIsInstance(FileStorage._FileStorage__objects, dict)

    def test_storage_initialization(self):
        self.assertIsInstance(models.storage, FileStorage)


class TestFileStorageFunctions(unittest.TestCase):
    """Tests for the functions in the FileStorage class."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "temp")
        except IOError:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("temp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all_returns_dict(self):
        self.assertIsInstance(models.storage.all(), dict)

    def test_all_with_argument_raises_error(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new_adds_objects(self):
        # Create one instance of each model
        instances = [BaseModel(), User(), State(), Place(), City(), Amenity(), Review()]
        for instance in instances:
            models.storage.new(instance)
            self.assertIn(f"{instance.__class__.__name__}.{instance.id}", models.storage.all())
            self.assertIn(instance, models.storage.all().values())

    def test_new_with_arguments_raises_error(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_new_with_None_raises_error(self):
        with self.assertRaises(AttributeError):
            models.storage.new(None)

    def test_save_creates_file(self):
        # Create and save new instances
        instances = [BaseModel(), User(), State(), Place(), City(), Amenity(), Review()]
        for instance in instances:
            models.storage.new(instance)
        models.storage.save()

        # Check if instances are saved in file
        with open("file.json", "r") as file:
            content = file.read()
            for instance in instances:
                self.assertIn(f"{instance.__class__.__name__}.{instance.id}", content)

    def test_save_with_argument_raises_error(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload_loads_objects(self):
        # Create and save new instances
        instances = [BaseModel(), User(), State(), Place(), City(), Amenity(), Review()]
        for instance in instances:
            models.storage.new(instance)
        models.storage.save()
        models.storage.reload()

        # Check if instances are reloaded correctly
        objects = FileStorage._FileStorage__objects
        for instance in instances:
            self.assertIn(f"{instance.__class__.__name__}.{instance.id}", objects)

    def test_reload_without_file_raises_error(self):
        self.assertRaises(FileNotFoundError, models.storage.reload())

    def test_reload_with_argument_raises_error(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
