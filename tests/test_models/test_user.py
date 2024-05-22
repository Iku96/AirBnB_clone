#!/usr/bin/python3
"""
Unit tests for the User class in models/user.py.

Test cases:
    TestUserCreation
    TestUserUpdate
    TestUserDictConversion
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class TestUserCreation(unittest.TestCase):
    """Tests for verifying the creation of User objects."""

    def test_creation_no_arguments(self):
        self.assertIsInstance(User(), User)

    def test_instance_in_storage(self):
        self.assertIn(User(), models.storage.all().values())

    def test_id_is_string(self):
        self.assertIsInstance(User().id, str)

    def test_created_at_is_datetime(self):
        self.assertIsInstance(User().created_at, datetime)

    def test_updated_at_is_datetime(self):
        self.assertIsInstance(User().updated_at, datetime)

    def test_email_attribute(self):
        self.assertIsInstance(User.email, str)

    def test_password_attribute(self):
        self.assertIsInstance(User.password, str)

    def test_first_name_attribute(self):
        self.assertIsInstance(User.first_name, str)

    def test_last_name_attribute(self):
        self.assertIsInstance(User.last_name, str)

    def test_unique_id_for_each_user(self):
        user1 = User()
        user2 = User()
        self.assertNotEqual(user1.id, user2.id)

    def test_different_creation_times(self):
        user1 = User()
        sleep(0.05)
        user2 = User()
        self.assertLess(user1.created_at, user2.created_at)

    def test_different_update_times(self):
        user1 = User()
        sleep(0.05)
        user2 = User()
        self.assertLess(user1.updated_at, user2.updated_at)

    def test_string_representation(self):
        current_time = datetime.today()
        time_repr = repr(current_time)
        user = User()
        user.id = "123456"
        user.created_at = user.updated_at = current_time
        user_str = str(user)
        self.assertIn("[User] (123456)", user_str)
        self.assertIn("'id': '123456'", user_str)
        self.assertIn("'created_at': " + time_repr, user_str)
        self.assertIn("'updated_at': " + time_repr, user_str)

    def test_unused_arguments(self):
        user = User(None)
        self.assertNotIn(None, user.__dict__.values())

    def test_creation_with_kwargs(self):
        current_time = datetime.today()
        time_iso = current_time.isoformat()
        user = User(id="345", created_at=time_iso, updated_at=time_iso)
        self.assertEqual(user.id, "345")
        self.assertEqual(user.created_at, current_time)
        self.assertEqual(user.updated_at, current_time)

    def test_creation_with_None_kwargs_raises_error(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUserUpdate(unittest.TestCase):
    """Tests for the update method of the User class."""

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
        user = User()
        sleep(0.05)
        first_update_time = user.updated_at
        user.save()
        self.assertLess(first_update_time, user.updated_at)

    def test_update_twice(self):
        user = User()
        sleep(0.05)
        first_update_time = user.updated_at
        user.save()
        second_update_time = user.updated_at
        self.assertLess(first_update_time, second_update_time)
        sleep(0.05)
        user.save()
        self.assertLess(second_update_time, user.updated_at)

    def test_update_with_argument_raises_error(self):
        user = User()
        with self.assertRaises(TypeError):
            user.save(None)

    def test_update_changes_file(self):
        user = User()
        user.save()
        user_id = "User." + user.id
        with open("file.json", "r") as file:
            self.assertIn(user_id, file.read())


class TestUserDictConversion(unittest.TestCase):
    """Tests for converting User instances to dictionaries."""

    def test_to_dict_returns_dict(self):
        self.assertIsInstance(User().to_dict(), dict)

    def test_to_dict_has_required_keys(self):
        user = User()
        self.assertIn("id", user.to_dict())
        self.assertIn("created_at", user.to_dict())
        self.assertIn("updated_at", user.to_dict())
        self.assertIn("__class__", user.to_dict())

    def test_to_dict_includes_extra_attributes(self):
        user = User()
        user.middle_name = "Holberton"
        user.my_number = 98
        self.assertIn("middle_name", user.to_dict())
        self.assertIn("my_number", user.to_dict())

    def test_datetime_attributes_in_dict_are_strings(self):
        user = User()
        user_dict = user.to_dict()
        self.assertIsInstance(user_dict["created_at"], str)
        self.assertIsInstance(user_dict["updated_at"], str)

    def test_to_dict_output_matches(self):
        current_time = datetime.today()
        user = User()
        user.id = "123456"
        user.created_at = user.updated_at = current_time
        expected_dict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': current_time.isoformat(),
            'updated_at': current_time.isoformat(),
        }
        self.assertDictEqual(user.to_dict(), expected_dict)

    def test_to_dict_vs_instance_dict(self):
        user = User()
        self.assertNotEqual(user.to_dict(), user.__dict__)

    def test_to_dict_with_argument_raises_error(self):
        user = User()
        with self.assertRaises(TypeError):
            user.to_dict(None)


if __name__ == "__main__":
    unittest.main()
