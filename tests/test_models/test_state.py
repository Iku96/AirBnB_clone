#!/usr/bin/python3
"""
Unit tests for the State class in models/state.py.

Test cases:
    TestStateCreation
    TestStateUpdate
    TestStateDictConversion
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class TestStateCreation(unittest.TestCase):
    """Tests for checking the instantiation of State objects."""

    def test_creation_no_arguments(self):
        self.assertIsInstance(State(), State)

    def test_instance_in_storage(self):
        self.assertIn(State(), models.storage.all().values())

    def test_id_is_string(self):
        self.assertIsInstance(State().id, str)

    def test_created_at_is_datetime(self):
        self.assertIsInstance(State().created_at, datetime)

    def test_updated_at_is_datetime(self):
        self.assertIsInstance(State().updated_at, datetime)

    def test_name_attribute(self):
        state = State()
        self.assertIsInstance(State.name, str)
        self.assertTrue(hasattr(state, 'name'))
        self.assertFalse('name' in state.__dict__)

    def test_unique_id_for_each_state(self):
        state1 = State()
        state2 = State()
        self.assertNotEqual(state1.id, state2.id)

    def test_different_creation_times(self):
        state1 = State()
        sleep(0.05)
        state2 = State()
        self.assertLess(state1.created_at, state2.created_at)

    def test_different_update_times(self):
        state1 = State()
        sleep(0.05)
        state2 = State()
        self.assertLess(state1.updated_at, state2.updated_at)

    def test_string_representation(self):
        current_time = datetime.today()
        time_repr = repr(current_time)
        state = State()
        state.id = "123456"
        state.created_at = state.updated_at = current_time
        state_str = str(state)
        self.assertIn("[State] (123456)", state_str)
        self.assertIn("'id': '123456'", state_str)
        self.assertIn("'created_at': " + time_repr, state_str)
        self.assertIn("'updated_at': " + time_repr, state_str)

    def test_unused_arguments(self):
        state = State(None)
        self.assertNotIn(None, state.__dict__.values())

    def test_creation_with_kwargs(self):
        current_time = datetime.today()
        time_iso = current_time.isoformat()
        state = State(id="345", created_at=time_iso, updated_at=time_iso)
        self.assertEqual(state.id, "345")
        self.assertEqual(state.created_at, current_time)
        self.assertEqual(state.updated_at, current_time)

    def test_creation_with_None_kwargs_raises_error(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestStateUpdate(unittest.TestCase):
    """Tests for the update method of the State class."""

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
        state = State()
        sleep(0.05)
        first_update_time = state.updated_at
        state.save()
        self.assertLess(first_update_time, state.updated_at)

    def test_update_twice(self):
        state = State()
        sleep(0.05)
        first_update_time = state.updated_at
        state.save()
        second_update_time = state.updated_at
        self.assertLess(first_update_time, second_update_time)
        sleep(0.05)
        state.save()
        self.assertLess(second_update_time, state.updated_at)

    def test_update_with_argument_raises_error(self):
        state = State()
        with self.assertRaises(TypeError):
            state.save(None)

    def test_update_changes_file(self):
        state = State()
        state.save()
        state_id = "State." + state.id
        with open("file.json", "r") as file:
            self.assertIn(state_id, file.read())


class TestStateDictConversion(unittest.TestCase):
    """Tests for converting State instances to dictionaries."""

    def test_to_dict_returns_dict(self):
        self.assertIsInstance(State().to_dict(), dict)

    def test_to_dict_has_required_keys(self):
        state = State()
        self.assertIn("id", state.to_dict())
        self.assertIn("created_at", state.to_dict())
        self.assertIn("updated_at", state.to_dict())
        self.assertIn("__class__", state.to_dict())

    def test_to_dict_includes_extra_attributes(self):
        state = State()
        state.middle_name = "Holberton"
        state.my_number = 98
        self.assertIn("middle_name", state.to_dict())
        self.assertIn("my_number", state.to_dict())

    def test_datetime_attributes_in_dict_are_strings(self):
        state = State()
        state_dict = state.to_dict()
        self.assertIsInstance(state_dict["created_at"], str)
        self.assertIsInstance(state_dict["updated_at"], str)

    def test_to_dict_output_matches(self):
        current_time = datetime.today()
        state = State()
        state.id = "123456"
        state.created_at = state.updated_at = current_time
        expected_dict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': current_time.isoformat(),
            'updated_at': current_time.isoformat(),
        }
        self.assertDictEqual(state.to_dict(), expected_dict)

    def test_to_dict_vs_instance_dict(self):
        state = State()
        self.assertNotEqual(state.to_dict(), state.__dict__)

    def test_to_dict_with_argument_raises_error(self):
        state = State()
        with self.assertRaises(TypeError):
            state.to_dict(None)


if __name__ == "__main__":
    unittest.main()
