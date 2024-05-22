#!/usr/bin/python3
"""
This module contains unit tests for the City class in models/city.py.

Test cases included:
    TestCityCreation
    TestCityUpdate
    TestCityDictRepresentation
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestCityCreation(unittest.TestCase):
    """Unit tests to verify the creation of City objects."""

    def test_creation_without_args(self):
        self.assertIsInstance(City(), City)

    def test_instance_is_stored(self):
        self.assertIn(City(), models.storage.all().values())

    def test_id_is_a_string(self):
        self.assertIsInstance(City().id, str)

    def test_created_at_is_datetime(self):
        self.assertIsInstance(City().created_at, datetime)

    def test_updated_at_is_datetime(self):
        self.assertIsInstance(City().updated_at, datetime)

    def test_state_id_attribute(self):
        city = City()
        self.assertIsInstance(City.state_id, str)
        self.assertTrue(hasattr(city, 'state_id'))
        self.assertFalse('state_id' in city.__dict__)

    def test_name_attribute(self):
        city = City()
        self.assertIsInstance(City.name, str)
        self.assertTrue(hasattr(city, 'name'))
        self.assertFalse('name' in city.__dict__)

    def test_unique_id_for_each_city(self):
        city1 = City()
        city2 = City()
        self.assertNotEqual(city1.id, city2.id)

    def test_different_creation_times(self):
        city1 = City()
        sleep(0.05)
        city2 = City()
        self.assertLess(city1.created_at, city2.created_at)

    def test_different_update_times(self):
        city1 = City()
        sleep(0.05)
        city2 = City()
        self.assertLess(city1.updated_at, city2.updated_at)

    def test_string_representation(self):
        current_time = datetime.today()
        time_repr = repr(current_time)
        city = City()
        city.id = "123456"
        city.created_at = city.updated_at = current_time
        city_str = str(city)
        self.assertIn("[City] (123456)", city_str)
        self.assertIn("'id': '123456'", city_str)
        self.assertIn("'created_at': " + time_repr, city_str)
        self.assertIn("'updated_at': " + time_repr, city_str)

    def test_unused_arguments(self):
        city = City(None)
        self.assertNotIn(None, city.__dict__.values())

    def test_creation_with_kwargs(self):
        current_time = datetime.today()
        time_iso = current_time.isoformat()
        city = City(id="345", created_at=time_iso, updated_at=time_iso)
        self.assertEqual(city.id, "345")
        self.assertEqual(city.created_at, current_time)
        self.assertEqual(city.updated_at, current_time)

    def test_creation_with_None_kwargs_raises_error(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCityUpdate(unittest.TestCase):
    """Unit tests for the update method of the City class."""

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
        city = City()
        sleep(0.05)
        first_update_time = city.updated_at
        city.save()
        self.assertLess(first_update_time, city.updated_at)

    def test_update_twice(self):
        city = City()
        sleep(0.05)
        first_update_time = city.updated_at
        city.save()
        second_update_time = city.updated_at
        self.assertLess(first_update_time, second_update_time)
        sleep(0.05)
        city.save()
        self.assertLess(second_update_time, city.updated_at)

    def test_update_with_argument_raises_error(self):
        city = City()
        with self.assertRaises(TypeError):
            city.save(None)

    def test_update_changes_file(self):
        city = City()
        city.save()
        city_id = "City." + city.id
        with open("file.json", "r") as file:
            self.assertIn(city_id, file.read())


class TestCityDictRepresentation(unittest.TestCase):
    """Unit tests for the dictionary representation of City objects."""

    def test_to_dict_returns_dict(self):
        self.assertIsInstance(City().to_dict(), dict)

    def test_to_dict_has_required_keys(self):
        city = City()
        self.assertIn("id", city.to_dict())
        self.assertIn("created_at", city.to_dict())
        self.assertIn("updated_at", city.to_dict())
        self.assertIn("__class__", city.to_dict())

    def test_to_dict_includes_extra_attributes(self):
        city = City()
        city.middle_name = "Holberton"
        city.my_number = 98
        self.assertIn("middle_name", city.to_dict())
        self.assertIn("my_number", city.to_dict())

    def test_datetime_attributes_in_dict_are_strings(self):
        city = City()
        city_dict = city.to_dict()
        self.assertIsInstance(city_dict["created_at"], str)
        self.assertIsInstance(city_dict["updated_at"], str)

    def test_to_dict_output_matches(self):
        current_time = datetime.today()
        city = City()
        city.id = "123456"
        city.created_at = city.updated_at = current_time
        expected_dict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': current_time.isoformat(),
            'updated_at': current_time.isoformat(),
        }
        self.assertDictEqual(city.to_dict(), expected_dict)

    def test_to_dict_vs_instance_dict(self):
        city = City()
        self.assertNotEqual(city.to_dict(), city.__dict__)

    def test_to_dict_with_argument_raises_error(self):
        city = City()
        with self.assertRaises(TypeError):
            city.to_dict(None)


if __name__ == "__main__":
    unittest.main()
