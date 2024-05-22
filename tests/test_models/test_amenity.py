#!/usr/bin/python3
"""
This script contains tests for the Amenity class in models/amenity.py.

Test groups:
    TestAmenityCreation
    TestAmenityUpdate
    TestAmenityDictionaryRepresentation
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity

class TestAmenityCreation(unittest.TestCase):
    """Tests to ensure Amenity objects are created correctly."""

    def test_creation_without_args(self):
        self.assertIsInstance(Amenity(), Amenity)

    def test_instance_in_storage(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_id_is_string(self):
        self.assertIsInstance(Amenity().id, str)

    def test_created_at_is_datetime(self):
        self.assertIsInstance(Amenity().created_at, datetime)

    def test_updated_at_is_datetime(self):
        self.assertIsInstance(Amenity().updated_at, datetime)

    def test_name_attribute(self):
        amenity = Amenity()
        self.assertIsInstance(Amenity.name, str)
        self.assertTrue(hasattr(amenity, 'name'))
        self.assertFalse('name' in amenity.__dict__)

    def test_unique_id_for_each_amenity(self):
        amenity1 = Amenity()
        amenity2 = Amenity()
        self.assertNotEqual(amenity1.id, amenity2.id)

    def test_different_creation_times(self):
        amenity1 = Amenity()
        sleep(0.05)
        amenity2 = Amenity()
        self.assertLess(amenity1.created_at, amenity2.created_at)

    def test_different_update_times(self):
        amenity1 = Amenity()
        sleep(0.05)
        amenity2 = Amenity()
        self.assertLess(amenity1.updated_at, amenity2.updated_at)

    def test_string_representation(self):
        current_time = datetime.today()
        time_repr = repr(current_time)
        amenity = Amenity()
        amenity.id = "123456"
        amenity.created_at = amenity.updated_at = current_time
        amenity_str = str(amenity)
        self.assertIn("[Amenity] (123456)", amenity_str)
        self.assertIn("'id': '123456'", amenity_str)
        self.assertIn("'created_at': " + time_repr, amenity_str)
        self.assertIn("'updated_at': " + time_repr, amenity_str)

    def test_unused_args(self):
        amenity = Amenity(None)
        self.assertNotIn(None, amenity.__dict__.values())

    def test_creation_with_kwargs(self):
        current_time = datetime.today()
        time_iso = current_time.isoformat()
        amenity = Amenity(id="345", created_at=time_iso, updated_at=time_iso)
        self.assertEqual(amenity.id, "345")
        self.assertEqual(amenity.created_at, current_time)
        self.assertEqual(amenity.updated_at, current_time)

    def test_creation_with_None_kwargs_raises_error(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)

class TestAmenityUpdate(unittest.TestCase):
    """Tests for the update functionality of the Amenity class."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "temp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("temp", "file.json")
        except IOError:
            pass

    def test_update_once(self):
        amenity = Amenity()
        sleep(0.05)
        initial_update_time = amenity.updated_at
        amenity.save()
        self.assertLess(initial_update_time, amenity.updated_at)

    def test_update_twice(self):
        amenity = Amenity()
        sleep(0.05)
        first_update_time = amenity.updated_at
        amenity.save()
        second_update_time = amenity.updated_at
        self.assertLess(first_update_time, second_update_time)
        sleep(0.05)
        amenity.save()
        self.assertLess(second_update_time, amenity.updated_at)

    def test_update_with_arg_raises_error(self):
        amenity = Amenity()
        with self.assertRaises(TypeError):
            amenity.save(None)

    def test_update_changes_file(self):
        amenity = Amenity()
        amenity.save()
        amenity_id = "Amenity." + amenity.id
        with open("file.json", "r") as file:
            self.assertIn(amenity_id, file.read())

class TestAmenityDictionaryRepresentation(unittest.TestCase):
    """Tests to check the dictionary representation of Amenity objects."""

    def test_to_dict_returns_dict(self):
        self.assertIsInstance(Amenity().to_dict(), dict)

    def test_to_dict_has_correct_keys(self):
        amenity = Amenity()
        self.assertIn("id", amenity.to_dict())
        self.assertIn("created_at", amenity.to_dict())
        self.assertIn("updated_at", amenity.to_dict())
        self.assertIn("__class__", amenity.to_dict())

    def test_to_dict_includes_custom_attrs(self):
        amenity = Amenity()
        amenity.middle_name = "Holberton"
        amenity.my_number = 98
        self.assertEqual(amenity.middle_name, "Holberton")
        self.assertIn("my_number", amenity.to_dict())

    def test_to_dict_datetime_as_strings(self):
        amenity = Amenity()
        amenity_dict = amenity.to_dict()
        self.assertIsInstance(amenity_dict["id"], str)
        self.assertIsInstance(amenity_dict["created_at"], str)
        self.assertIsInstance(amenity_dict["updated_at"], str)

    def test_to_dict_correct_output(self):
        current_time = datetime.today()
        amenity = Amenity()
        amenity.id = "123456"
        amenity.created_at = amenity.updated_at = current_time
        expected_dict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': current_time.isoformat(),
            'updated_at': current_time.isoformat(),
        }
        self.assertDictEqual(amenity.to_dict(), expected_dict)

    def test_to_dict_vs_dunder_dict(self):
        amenity = Amenity()
        self.assertNotEqual(amenity.to_dict(), amenity.__dict__)

    def test_to_dict_with_arg_raises_error(self):
        amenity = Amenity()
        with self.assertRaises(TypeError):
            amenity.to_dict(None)


if __name__ == "__main__":
    unittest.main()
