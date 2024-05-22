#!/usr/bin/python3
"""
This script is for unit testing the BaseModel class in models/base_model.py.

Tests included:
    TestBaseModelCreation
    TestBaseModelUpdate
    TestBaseModelDictConversion
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel

class TestBaseModelCreation(unittest.TestCase):
    """Tests for verifying the creation of BaseModel instances."""

    def test_creation_no_arguments(self):
        self.assertIs(type(BaseModel()), BaseModel)

    def test_instance_in_storage(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_public_string(self):
        self.assertIs(type(BaseModel().id), str)

    def test_created_at_public_datetime(self):
        self.assertIs(type(BaseModel().created_at), datetime)

    def test_updated_at_public_datetime(self):
        self.assertIs(type(BaseModel().updated_at), datetime)

    def test_unique_ids_for_models(self):
        base_model_1 = BaseModel()
        base_model_2 = BaseModel()
        self.assertNotEqual(base_model_1.id, base_model_2.id)

    def test_different_creation_times_for_models(self):
        base_model_1 = BaseModel()
        sleep(0.05)
        base_model_2 = BaseModel()
        self.assertLess(base_model_1.created_at, base_model_2.created_at)

    def test_different_update_times_for_models(self):
        base_model_1 = BaseModel()
        sleep(0.05)
        base_model_2 = BaseModel()
        self.assertLess(base_model_1.updated_at, base_model_2.updated_at)

    def test_string_output(self):
        current_time = datetime.today()
        time_representation = repr(current_time)
        base_model = BaseModel()
        base_model.id = "123456"
        base_model.created_at = base_model.updated_at = current_time
        base_model_string = base_model.__str__()
        self.assertIn("[BaseModel] (123456)", base_model_string)
        self.assertIn("'id': '123456'", base_model_string)
        self.assertIn("'created_at': " + time_representation, base_model_string)
        self.assertIn("'updated_at': " + time_representation, base_model_string)

    def test_unused_arguments(self):
        base_model = BaseModel(None)
        self.assertNotIn(None, base_model.__dict__.values())

    def test_creation_with_keyword_arguments(self):
        current_time = datetime.today()
        time_iso = current_time.isoformat()
        base_model = BaseModel(id="345", created_at=time_iso, updated_at=time_iso)
        self.assertEqual(base_model.id, "345")
        self.assertEqual(base_model.created_at, current_time)
        self.assertEqual(base_model.updated_at, current_time)

    def test_creation_with_None_keyword_arguments(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_creation_with_args_and_kwargs(self):
        current_time = datetime.today()
        time_iso = current_time.isoformat()
        base_model = BaseModel("12", id="345", created_at=time_iso, updated_at=time_iso)
        self.assertEqual(base_model.id, "345")
        self.assertEqual(base_model.created_at, current_time)
        self.assertEqual(base_model.updated_at, current_time)

class TestBaseModelUpdate(unittest.TestCase):
    """Tests for the update method of the BaseModel class."""

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

    def test_single_update(self):
        base_model = BaseModel()
        sleep(0.05)
        initial_update_time = base_model.updated_at
        base_model.save()
        self.assertLess(initial_update_time, base_model.updated_at)

    def test_multiple_updates(self):
        base_model = BaseModel()
        sleep(0.05)
        first_update_time = base_model.updated_at
        base_model.save()
        second_update_time = base_model.updated_at
        self.assertLess(first_update_time, second_update_time)
        sleep(0.05)
        base_model.save()
        self.assertLess(second_update_time, base_model.updated_at)

    def test_update_with_argument(self):
        base_model = BaseModel()
        with self.assertRaises(TypeError):
            base_model.save(None)

    def test_update_changes_file_content(self):
        base_model = BaseModel()
        base_model.save()
        base_model_id = "BaseModel." + base_model.id
        with open("file.json", "r") as file:
            self.assertIn(base_model_id, file.read())

class TestBaseModelDictConversion(unittest.TestCase):
    """Tests for converting BaseModel instances to dictionaries."""

    def test_dict_conversion_returns_dict(self):
        self.assertIsInstance(BaseModel().to_dict(), dict)

    def test_dict_contains_correct_keys(self):
        base_model = BaseModel()
        self.assertIn("id", base_model.to_dict())
        self.assertIn("created_at", base_model.to_dict())
        self.assertIn("updated_at", base_model.to_dict())
        self.assertIn("__class__", base_model.to_dict())

    def test_dict_includes_custom_attributes(self):
        base_model = BaseModel()
        base_model.name = "Holberton"
        base_model.my_number = 98
        self.assertIn("name", base_model.to_dict())
        self.assertIn("my_number", base_model.to_dict())

    def test_datetime_attributes_as_strings_in_dict(self):
        base_model = BaseModel()
        base_model_dict = base_model.to_dict()
        self.assertIsInstance(base_model_dict["created_at"], str)
        self.assertIsInstance(base_model_dict["updated_at"], str)

    def test_dict_output_matches_expected(self):
        current_time = datetime.today()
        base_model = BaseModel()
        base_model.id = "123456"
        base_model.created_at = base_model.updated_at = current_time
        expected_dict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': current_time.isoformat(),
            'updated_at': current_time.isoformat()
        }
        self.assertDictEqual(base_model.to_dict(), expected_dict)

    def test_dict_vs_instance_attributes(self):
        base_model = BaseModel()
        self.assertNotEqual(base_model.to_dict(), base_model.__dict__)

    def test_dict_conversion_with_argument(self):
        base_model = BaseModel()
        with self.assertRaises(TypeError):
            base_model.to_dict(None)


if __name__ == "__main__":
    unittest.main()
