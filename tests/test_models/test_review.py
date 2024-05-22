#!/usr/bin/python3
"""
Unit tests for the Review class in models/review.py.

Test cases:
    TestReviewCreation
    TestReviewUpdate
    TestReviewDictConversion
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.review import Review


class TestReviewCreation(unittest.TestCase):
    """Tests for checking the instantiation of Review objects."""

    def test_creation_no_arguments(self):
        self.assertIsInstance(Review(), Review)

    def test_instance_in_storage(self):
        self.assertIn(Review(), models.storage.all().values())

    def test_id_is_string(self):
        self.assertIsInstance(Review().id, str)

    def test_created_at_is_datetime(self):
        self.assertIsInstance(Review().created_at, datetime)

    def test_updated_at_is_datetime(self):
        self.assertIsInstance(Review().updated_at, datetime)

    def test_place_id_attribute(self):
        review = Review()
        self.assertIsInstance(Review.place_id, str)
        self.assertTrue(hasattr(review, 'place_id'))
        self.assertFalse('place_id' in review.__dict__)

    def test_user_id_attribute(self):
        review = Review()
        self.assertIsInstance(Review.user_id, str)
        self.assertTrue(hasattr(review, 'user_id'))
        self.assertFalse('user_id' in review.__dict__)

    def test_text_attribute(self):
        review = Review()
        self.assertIsInstance(Review.text, str)
        self.assertTrue(hasattr(review, 'text'))
        self.assertFalse('text' in review.__dict__)

    def test_unique_id_for_each_review(self):
        review1 = Review()
        review2 = Review()
        self.assertNotEqual(review1.id, review2.id)

    def test_different_creation_times(self):
        review1 = Review()
        sleep(0.05)
        review2 = Review()
        self.assertLess(review1.created_at, review2.created_at)

    def test_different_update_times(self):
        review1 = Review()
        sleep(0.05)
        review2 = Review()
        self.assertLess(review1.updated_at, review2.updated_at)

    def test_string_representation(self):
        current_time = datetime.today()
        time_repr = repr(current_time)
        review = Review()
        review.id = "123456"
        review.created_at = review.updated_at = current_time
        review_str = str(review)
        self.assertIn("[Review] (123456)", review_str)
        self.assertIn("'id': '123456'", review_str)
        self.assertIn("'created_at': " + time_repr, review_str)
        self.assertIn("'updated_at': " + time_repr, review_str)

    def test_unused_arguments(self):
        review = Review(None)
        self.assertNotIn(None, review.__dict__.values())

    def test_creation_with_kwargs(self):
        current_time = datetime.today()
        time_iso = current_time.isoformat()
        review = Review(id="345", created_at=time_iso, updated_at=time_iso)
        self.assertEqual(review.id, "345")
        self.assertEqual(review.created_at, current_time)
        self.assertEqual(review.updated_at, current_time)

    def test_creation_with_None_kwargs_raises_error(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReviewUpdate(unittest.TestCase):
    """Tests for the update method of the Review class."""

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
        review = Review()
        sleep(0.05)
        first_update_time = review.updated_at
        review.save()
        self.assertLess(first_update_time, review.updated_at)

    def test_update_twice(self):
        review = Review()
        sleep(0.05)
        first_update_time = review.updated_at
        review.save()
        second_update_time = review.updated_at
        self.assertLess(first_update_time, second_update_time)
        sleep(0.05)
        review.save()
        self.assertLess(second_update_time, review.updated_at)

    def test_update_with_argument_raises_error(self):
        review = Review()
        with self.assertRaises(TypeError):
            review.save(None)

    def test_update_changes_file(self):
        review = Review()
        review.save()
        review_id = "Review." + review.id
        with open("file.json", "r") as file:
            self.assertIn(review_id, file.read())


class TestReviewDictConversion(unittest.TestCase):
    """Tests for converting Review instances to dictionaries."""

    def test_to_dict_returns_dict(self):
        self.assertIsInstance(Review().to_dict(), dict)

    def test_to_dict_has_required_keys(self):
        review = Review()
        self.assertIn("id", review.to_dict())
        self.assertIn("created_at", review.to_dict())
        self.assertIn("updated_at", review.to_dict())
        self.assertIn("__class__", review.to_dict())

    def test_to_dict_includes_extra_attributes(self):
        review = Review()
        review.middle_name = "Betty"
        review.my_number = 98
        self.assertIn("middle_name", review.to_dict())
        self.assertIn("my_number", review.to_dict())

    def test_datetime_attributes_in_dict_are_strings(self):
        review = Review()
        review_dict = review.to_dict()
        self.assertIsInstance(review_dict["created_at"], str)
        self.assertIsInstance(review_dict["updated_at"], str)

    def test_to_dict_output_matches(self):
        current_time = datetime.today()
        review = Review()
        review.id = "123456"
        review.created_at = review.updated_at = current_time
        expected_dict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': current_time.isoformat(),
            'updated_at': current_time.isoformat(),
        }
        self.assertDictEqual(review.to_dict(), expected_dict)

    def test_to_dict_vs_instance_dict(self):
        review = Review()
        self.assertNotEqual(review.to_dict(), review.__dict__)

    def test_to_dict_with_argument_raises_error(self):
        review = Review()
        with self.assertRaises(TypeError):
            review.to_dict(None)


if __name__ == "__main__":
    unittest.main()
