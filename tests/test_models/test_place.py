#!/usr/bin/python3
"""
This module contains unit tests for the Place class in models/place.py.

Test cases included:
    TestPlaceCreation
    TestPlaceUpdate
    TestPlaceDictRepresentation
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place


class TestPlaceCreation(unittest.TestCase):
    """Unit tests to verify the creation of Place objects."""

    def test_creation_without_args(self):
        self.assertIs(type(Place()), Place)

    def test_instance_is_stored(self):
        self.assertIn(Place(), models.storage.all().values())

    def test_id_is_a_string(self):
        self.assertIs(type(Place().id), str)

    def test_created_at_is_datetime(self):
        self.assertIs(type(Place().created_at), datetime)

    def test_updated_at_is_datetime(self):
        self.assertIs(type(Place().updated_at), datetime)

    def test_city_id_attribute(self):
        place = Place()
        self.assertIs(type(Place.city_id), str)
        self.assertTrue(hasattr(place, 'city_id'))
        self.assertFalse('city_id' in place.__dict__)

    def test_user_id_attribute(self):
        place = Place()
        self.assertIs(type(Place.user_id), str)
        self.assertTrue(hasattr(place, 'user_id'))
        self.assertFalse('user_id' in place.__dict__)

    def test_name_attribute(self):
        place = Place()
        self.assertIs(type(Place.name), str)
        self.assertTrue(hasattr(place, 'name'))
        self.assertFalse('name' in place.__dict__)

    def test_description_attribute(self):
        place = Place()
        self.assertIs(type(Place.description), str)
        self.assertTrue(hasattr(place, 'description'))
        self.assertFalse('description' in place.__dict__)

    def test_number_rooms_attribute(self):
        place = Place()
        self.assertIs(type(Place.number_rooms), int)
        self.assertTrue(hasattr(place, 'number_rooms'))
        self.assertFalse('number_rooms' in place.__dict__)

    def test_number_bathrooms_attribute(self):
        place = Place()
        self.assertIs(type(Place.number_bathrooms), int)
        self.assertTrue(hasattr(place, 'number_bathrooms'))
        self.assertFalse('number_bathrooms' in place.__dict__)

    def test_max_guest_attribute(self):
        place = Place()
        self.assertIs(type(Place.max_guest), int)
        self.assertTrue(hasattr(place, 'max_guest'))
        self.assertFalse('max_guest' in place.__dict__)

    def test_price_by_night_attribute(self):
        place = Place()
        self.assertIs(type(Place.price_by_night), int)
        self.assertTrue(hasattr(place, 'price_by_night'))
        self.assertFalse('price_by_night' in place.__dict__)

    def test_latitude_attribute(self):
        place = Place()
        self.assertIs(type(Place.latitude), float)
        self.assertTrue(hasattr(place, 'latitude'))
        self.assertFalse('latitude' in place.__dict__)

    def test_longitude_attribute(self):
        place = Place()
        self.assertIs(type(Place.longitude), float)
        self.assertTrue(hasattr(place, 'longitude'))
        self.assertFalse('longitude' in place.__dict__)

    def test_amenity_ids_attribute(self):
        place = Place()
        self.assertIs(type(Place.amenity_ids), list)
        self.assertTrue(hasattr(place, 'amenity_ids'))
        self.assertFalse('amenity_ids' in place.__dict__)

    def test_unique_id_for_each_place(self):
        place1 = Place()
        place2 = Place()
        self.assertNotEqual(place1.id, place2.id)

    def test_different_creation_times(self):
        place1 = Place()
        sleep(0.05)
        place2 = Place()
        self.assertLess(place1.created_at, place2.created_at)

    def test_different_update_times(self):
        place1 = Place()
        sleep(0.05)
        place2 = Place()
        self.assertLess(place1.updated_at, place2.updated_at)

    def test_string_representation(self):
        current_time = datetime.today()
        time_repr = repr(current_time)
        place = Place()
        place.id = "123456"
        place.created_at = place.updated_at = current_time
        place_str = str(place)
        self.assertIn("[Place] (123456)", place_str)
        self.assertIn("'id': '123456'", place_str)
        self.assertIn("'created_at': " + time_repr, place_str)
        self.assertIn("'updated_at': " + time_repr, place_str)

    def test_unused_arguments(self):
        place = Place(None)
        self.assertNotIn(None, place.__dict__.values())

    def test_creation_with_kwargs(self):
        current_time = datetime.today()
        time_iso = current_time.isoformat()
        place = Place(id="345", created_at=time_iso, updated_at=time_iso)
        self.assertEqual(place.id, "345")
        self.assertEqual(place.created_at, current_time)
        self.assertEqual(place.updated_at, current_time)

    def test_creation_with_None_kwargs_raises_error(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlaceUpdate(unittest.TestCase):
    """Unit tests for the update method of the Place class."""

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
        place = Place()
        sleep(0.05)
        first_update_time = place.updated_at
        place.save()
        self.assertLess(first_update_time, place.updated_at)

    def test_update_twice(self):
        place = Place()
        sleep(0.05)
        first_update_time = place.updated_at
        place.save()
        second_update_time = place.updated_at
        self.assertLess(first_update_time, second_update_time)
        sleep(0.05)
        place.save()
        self.assertLess(second_update_time, place.updated_at)

    def test_update_with_argument_raises_error(self):
        place = Place()
        with self.assertRaises(TypeError):
            place.save(None)

    def test_update_changes_file(self):
        place = Place()
        place.save()
        place_id = "Place." + place.id
        with open("file.json", "r") as file:
            self.assertIn(place_id, file.read())


class TestPlaceDictRepresentation(unittest.TestCase):
    """Unit tests for the dictionary representation of Place objects."""

    def test_to_dict_returns_dict(self):
        self.assertIsInstance(Place().to_dict(), dict)

    def test_to_dict_has_required_keys(self):
        place = Place()
        self.assertIn("id", place.to_dict())
        self.assertIn("created_at", place.to_dict())
        self.assertIn("updated_at", place.to_dict())
        self.assertIn("__class__", place.to_dict())

    def test_to_dict_includes_extra_attributes(self):
        place = Place()
        place.middle_name = "Holberton"
        place.my_number = 98
        self.assertIn("middle_name", place.to_dict())
        self.assertIn("my_number", place.to_dict())

    def test_datetime_attributes_in_dict_are_strings(self):
        place = Place()
        place_dict = place.to_dict()
        self.assertIsInstance(place_dict["created_at"], str)
        self.assertIsInstance(place_dict["updated_at"], str)

    def test_to_dict_output_matches(self):
        current_time = datetime.today()
        place = Place()
        place.id = "123456"
        place.created_at = place.updated_at = current_time
        expected_dict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': current_time.isoformat(),
            'updated_at': current_time.isoformat(),
        }
        self.assertDictEqual(place.to_dict(), expected_dict)

    def test_to_dict_vs_instance_dict(self):
        place = Place()
        self.assertNotEqual(place.to_dict(), place.__dict__)

    def test_to_dict_with_argument_raises_error(self):
        place = Place()
        with self.assertRaises(TypeError):
            place.to_dict(None)


if __name__ == "__main__":
    unittest.main()
