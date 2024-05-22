#!/usr/bin/python3
"""
Contains unit tests for the console.py module.

Classes included for testing:
    - TestHBNBCommandPrompting
    - TestHBNBCommandHelp
    - TestHBNBCommandExit
    - TestHBNBCommandCreate
    - TestHBNBCommandShow
    - TestHBNBCommandAll
    - TestHBNBCommandDestroy
    - TestHBNBCommandUpdate
"""

import os
import sys
import unittest
from models import storage
from models.engine.file_storage import FileStorage
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch


class TestHBNBCommandPrompting(unittest.TestCase):
    """Tests for the prompt behavior of the AirBnB clone command interpreter."""

    def test_prompt_display(self):
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_handle_empty_line(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", output.getvalue().strip())


class TestHBNBCommandHelp(unittest.TestCase):
    """Tests for the help messages in the AirBnB clone command interpreter."""

    def test_quit_help_message(self):
        expected_output = "Quit command to exit the program."
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(expected_output, output.getvalue().strip())

    def test_create_help_message(self):
        expected_output = ("Usage: create <class>\n        "
                           "Create a new class instance and print its id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help create"))
            self.assertEqual(expected_output, output.getvalue().strip())

    def test_eof_help_message(self):
        expected_output = "EOF signal to exit the program."
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help EOF"))
            self.assertEqual(expected_output, output.getvalue().strip())

    def test_show_help_message(self):
        expected_output = ("Usage: show <class> <id> or <class>.show(<id>)\n        "
                           "Display the string representation of a class instance of"
                           " a given id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help show"))
            self.assertEqual(expected_output, output.getvalue().strip())

    def test_destroy_help_message(self):
        expected_output = ("Usage: destroy <class> <id> or <class>.destroy(<id>)\n        "
                           "Delete a class instance of a given id.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help destroy"))
            self.assertEqual(expected_output, output.getvalue().strip())

    def test_all_help_message(self):
        expected_output = ("Usage: all or all <class> or <class>.all()\n        "
                           "Display string representations of all instances of a given class"
                           ".\n        If no class is specified, displays all instantiated "
                           "objects.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help all"))
            self.assertEqual(expected_output, output.getvalue().strip())

    def test_count_help_message(self):
        expected_output = ("Usage: count <class> or <class>.count()\n        "
                           "Retrieve the number of instances of a given class.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help count"))
            self.assertEqual(expected_output, output.getvalue().strip())

    def test_update_help_message(self):
        expected_output = ("Usage: update <class> <id> <attribute_name> <attribute_value> or"
                           "\n       <class>.update(<id>, <attribute_name>, <attribute_value"
                           ">) or\n       <class>.update(<id>, <dictionary>)\n        "
                           "Update a class instance of a given id by adding or updating\n   "
                           "     a given attribute key/value pair or dictionary.")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help update"))
            self.assertEqual(expected_output, output.getvalue().strip())

    def test_general_help(self):
        expected_output = ("Documented commands (type help <topic>):\n"
                           "========================================\n"
                           "EOF  all  count  create  destroy  help  quit  show  update")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(expected_output, output.getvalue().strip())


class TestHBNBCommandExit(unittest.TestCase):
    """Tests for exit commands in the AirBnB clone command interpreter."""

    def test_quit_command(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_eof_command(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("EOF"))


class TestHBNBCommandCreate(unittest.TestCase):
    """Tests for the create command in the AirBnB clone command interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_create_without_class(self):
        expected_output = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(expected_output, output.getvalue().strip())

    def test_create_with_invalid_class(self):
        expected_output = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create MyModel"))
            self.assertEqual(expected_output, output.getvalue().strip())

    def test_invalid_syntax_create(self):
        expected_output = "*** Unknown syntax: MyModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.create()"))
            self.assertEqual(expected_output, output.getvalue().strip())
        expected_output = "*** Unknown syntax: BaseModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.create()"))
            self.assertEqual(expected_output, output.getvalue().strip())

    def test_create_object(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertGreater(len(output.getvalue().strip()), 0)
            testKey = "BaseModel.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertGreater(len(output.getvalue().strip()), 0)
            testKey = "User.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertGreater(len(output.getvalue().strip()), 0)
            testKey = "State.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertGreater(len(output.getvalue().strip()), 0)
            testKey = "City.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertGreater(len(output.getvalue().strip()), 0)
            testKey = "Amenity.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertGreater(len(output.getvalue().strip()), 0)
            testKey = "Place.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            self.assertGreater(len(output.getvalue().strip()), 0)
            testKey = "Review.{}".format(output.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())

    class TestHBNBCommandShow(unittest.TestCase):
        """Unit tests for the show command in the AirBnB clone command interpreter"""

        @classmethod
        def setUp(cls):
            try:
                os.rename("file.json", "tmp")
            except IOError:
                pass
            FileStorage.__objects = {}

        @classmethod
        def tearDown(cls):
            try:
                os.remove("file.json")
            except IOError:
                pass
            try:
                os.rename("tmp", "file.json")
            except IOError:
                pass

        def test_show_missing_class(self):
            expected_output = "** class name missing **"
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("show"))
                self.assertEqual(expected_output, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(".show()"))
                self.assertEqual(expected_output, output.getvalue().strip())

        def test_show_invalid_class(self):
            expected_output = "** class doesn't exist **"
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("show MyModel"))
                self.assertEqual(expected_output, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("MyModel.show()"))
                self.assertEqual(expected_output, output.getvalue().strip())

        def test_show_missing_id_space_notation(self):
            expected_output = "** instance id missing **"
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("show BaseModel"))
                self.assertEqual(expected_output, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("show User"))
                self.assertEqual(expected_output, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("show State"))
                self.assertEqual(expected_output, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("show City"))
                self.assertEqual(expected_output, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("show Amenity"))
                self.assertEqual(expected_output, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("show Place"))
                self.assertEqual(expected_output, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("show Review"))
                self.assertEqual(expected_output, output.getvalue().strip())

        def test_show_missing_id_dot_notation(self):
            expected_output = "** instance id missing **"
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("BaseModel.show()"))
                self.assertEqual(expected_output, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("User.show()"))
                self.assertEqual(expected_output, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("State.show()"))
                self.assertEqual(expected_output, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("City.show()"))
                self.assertEqual(expected_output, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("Amenity.show()"))
                self.assertEqual(expected_output, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("Place.show()"))
                self.assertEqual(expected_output, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("Review.show()"))
                self.assertEqual(expected_output, output.getvalue().strip())

        def test_show_instance_not_found_space_notation(self):
            expected_output = "** no instance found **"
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("show BaseModel 1"))
                self.assertEqual(expected_output, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("show User 1"))
                self.assertEqual(expected_output, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("show State 1"))
                self.assertEqual(expected_output, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("show City 1"))
                self.assertEqual(expected_output, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("show Amenity 1"))
                self.assertEqual(expected_output, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("show Place 1"))
                self.assertEqual(expected_output, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("show Review 1"))
                self.assertEqual(expected_output, output.getvalue().strip())

        def test_show_no_instance_found_dot_notation(self):
            correct = "** no instance found **"
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("BaseModel.show(1)"))
                self.assertEqual(correct, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("User.show(1)"))
                self.assertEqual(correct, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("State.show(1)"))
                self.assertEqual(correct, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("City.show(1)"))
                self.assertEqual(correct, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("Amenity.show(1)"))
                self.assertEqual(correct, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("Place.show(1)"))
                self.assertEqual(correct, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("Review.show(1)"))
                self.assertEqual(correct, output.getvalue().strip())

        def test_show_objects_space_notation(self):
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
                testID = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                obj = storage.all()["BaseModel.{}".format(testID)]
                command = "show BaseModel {}".format(testID)
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(obj.__str__(), output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create User"))
                testID = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                obj = storage.all()["User.{}".format(testID)]
                command = "show User {}".format(testID)
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(obj.__str__(), output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create State"))
                testID = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                obj = storage.all()["State.{}".format(testID)]
                command = "show State {}".format(testID)
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(obj.__str__(), output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create Place"))
                testID = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                obj = storage.all()["Place.{}".format(testID)]
                command = "show Place {}".format(testID)
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(obj.__str__(), output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create City"))
                testID = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                obj = storage.all()["City.{}".format(testID)]
                command = "show City {}".format(testID)
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(obj.__str__(), output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create Amenity"))
                testID = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                obj = storage.all()["Amenity.{}".format(testID)]
                command = "show Amenity {}".format(testID)
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(obj.__str__(), output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create Review"))
                testID = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                obj = storage.all()["Review.{}".format(testID)]
                command = "show Review {}".format(testID)
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(obj.__str__(), output.getvalue().strip())

        def test_show_instance_with_space_notation(self):
            """Test displaying an instance using space notation."""
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
                instance_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                instance = storage.all()[f"BaseModel.{instance_id}"]
                command = f"show BaseModel {instance_id}"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(str(instance), output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create User"))
                instance_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                instance = storage.all()[f"User.{instance_id}"]
                command = f"show User {instance_id}"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(str(instance), output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create State"))
                instance_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                instance = storage.all()[f"State.{instance_id}"]
                command = f"show State {instance_id}"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(str(instance), output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create City"))
                instance_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                instance = storage.all()[f"City.{instance_id}"]
                command = f"show City {instance_id}"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(str(instance), output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create Amenity"))
                instance_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                instance = storage.all()[f"Amenity.{instance_id}"]
                command = f"show Amenity {instance_id}"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(str(instance), output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
                instance_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                instance = storage.all()[f"BaseModel.{instance_id}"]
                command = f"show BaseModel {instance_id}"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(str(instance), output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create Place"))
                instance_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                instance = storage.all()[f"Place.{instance_id}"]
                command = f"show Place {instance_id}"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(str(instance), output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create Review"))
                instance_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                instance = storage.all()[f"Review.{instance_id}"]
                command = f"show Review {instance_id}"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(str(instance), output.getvalue().strip())

    class TestHBNBCommandDestroy(unittest.TestCase):
        """Tests for destroying instances with the 'destroy' command
        in the AirBnB clone command interpreter."""

        @classmethod
        def setUpClass(cls):
            """Set up the environment before running 'destroy' command tests."""
            try:
                os.rename("file.json", "tmp")
            except IOError:
                pass
            FileStorage._FileStorage__objects = {}

        @classmethod
        def tearDownClass(cls):
            """Clean up the environment after running 'destroy' command tests."""
            try:
                os.remove("file.json")
            except IOError:
                pass
            try:
                os.rename("tmp", "file.json")
            except IOError:
                pass
            storage.reload()

        def test_destroy_command_without_class_name(self):
            """Test the 'destroy' command without specifying a class name."""
            expected_message = "** class name missing **"
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("destroy"))
                self.assertEqual(expected_message, output.getvalue().strip())

        def test_destroy_command_with_nonexistent_class(self):
            """Test the 'destroy' command with a class that doesn't exist."""
            expected_message = "** class doesn't exist **"
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("destroy MyModel"))
                self.assertEqual(expected_message, output.getvalue().strip())

        def test_destroy_command_without_id_space_notation(self):
            """Test the 'destroy' command without providing an instance ID using space notation."""
            expected_message = "** instance id missing **"
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("destroy BaseModel"))
                self.assertEqual(expected_message, output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("destroy User"))
                self.assertEqual(expected_message, output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("destroy State"))
                self.assertEqual(expected_message, output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("destroy City"))
                self.assertEqual(expected_message, output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("destroy Amenity"))
                self.assertEqual(expected_message, output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("destroy Place"))
                self.assertEqual(expected_message, output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("destroy Review"))
                self.assertEqual(expected_message, output.getvalue().strip())

        def test_destroy_command_without_id_dot_notation(self):
            """Test the 'destroy' command without providing an instance ID using dot notation."""
            expected_message = "** instance id missing **"
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy()"))
                self.assertEqual(expected_message, output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("User.destroy()"))
                self.assertEqual(expected_message, output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("State.destroy()"))
                self.assertEqual(expected_message, output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("City.destroy()"))
                self.assertEqual(expected_message, output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("Amenity.destroy()"))
                self.assertEqual(expected_message, output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("Place.destroy()"))
                self.assertEqual(expected_message, output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("Review.destroy()"))
                self.assertEqual(expected_message, output.getvalue().strip())

        def test_destroy_command_with_invalid_id_space_notation(self):
            """Test the 'destroy' command with an invalid instance ID using space notation."""
            expected_message = "** no instance found **"
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("destroy BaseModel 1"))
                self.assertEqual(expected_message, output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("destroy User 1"))
                self.assertEqual(expected_message, output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("destroy State 1"))
                self.assertEqual(expected_message, output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("destroy City 1"))
                self.assertEqual(expected_message, output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("destroy Amenity 1"))
                self.assertEqual(expected_message, output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("destroy Place 1"))
                self.assertEqual(expected_message, output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("destroy Review 1"))
                self.assertEqual(expected_message, output.getvalue().strip())

        def test_destroy_command_with_invalid_id_dot_notation(self):
            """Test the 'destroy' command with an invalid instance ID using dot notation."""
            expected_message = "** no instance found **"
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy(1)"))
                self.assertEqual(expected_message, output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("User.destroy(1)"))
                self.assertEqual(expected_message, output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("State.destroy(1)"))
                self.assertEqual(expected_message, output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("City.destroy(1)"))
                self.assertEqual(expected_message, output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("Amenity.destroy(1)"))
                self.assertEqual(expected_message, output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("Place.destroy(1)"))
                self.assertEqual(expected_message, output.getvalue().strip())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("Review.destroy(1)"))
                self.assertEqual(expected_message, output.getvalue().strip())

        def test_destroy_existing_objects_space_notation(self):
            """Test the 'destroy' command on existing objects using space notation."""
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
                instance_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                instance = storage.all()[f"BaseModel.{instance_id}"]
                command = f"destroy BaseModel {instance_id}"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertNotIn(instance, storage.all())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create User"))
                instance_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                instance = storage.all()[f"User.{instance_id}"]
                command = f"destroy User {instance_id}"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertNotIn(instance, storage.all())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create State"))
                instance_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                instance = storage.all()[f"State.{instance_id}"]
                command = f"destroy State {instance_id}"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertNotIn(instance, storage.all())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create City"))
                instance_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                instance = storage.all()[f"City.{instance_id}"]
                command = f"destroy City {instance_id}"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertNotIn(instance, storage.all())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create Amenity"))
                instance_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                instance = storage.all()[f"Amenity.{instance_id}"]
                command = f"destroy Amenity {instance_id}"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertNotIn(instance, storage.all())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create Place"))
                instance_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                instance = storage.all()[f"Place.{instance_id}"]
                command = f"destroy Place {instance_id}"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertNotIn(instance, storage.all())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create Review"))
                instance_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                instance = storage.all()[f"Review.{instance_id}"]
                command = f"destroy Review {instance_id}"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertNotIn(instance, storage.all())

        def test_destroy_existing_objects_dot_notation(self):
            """Test the 'destroy' command on existing objects using dot notation."""
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
                instance_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                instance = storage.all()[f"BaseModel.{instance_id}"]
                command = f"BaseModel.destroy({instance_id})"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertNotIn(instance, storage.all())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create User"))
                instance_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                instance = storage.all()[f"User.{instance_id}"]
                command = f"User.destroy({instance_id})"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertNotIn(instance, storage.all())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create State"))
                instance_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                instance = storage.all()[f"State.{instance_id}"]
                command = f"State.destroy({instance_id})"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertNotIn(instance, storage.all())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create City"))
                instance_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                instance = storage.all()[f"City.{instance_id}"]
                command = f"City.destroy({instance_id})"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertNotIn(instance, storage.all())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create Amenity"))
                instance_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                instance = storage.all()[f"Amenity.{instance_id}"]
                command = f"Amenity.destroy({instance_id})"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertNotIn(instance, storage.all())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create Place"))
                instance_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                instance = storage.all()[f"Place.{instance_id}"]
                command = f"Place.destroy({instance_id})"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertNotIn(instance, storage.all())

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create Review"))
                instance_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as output:
                instance = storage.all()[f"Review.{instance_id}"]
                command = f"Review.destroy({instance_id})"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertNotIn(instance, storage.all())

    class TestHBNBCommandAll(unittest.TestCase):
        """Unit tests for the 'all' command in the AirBnB clone command interpreter."""

        @classmethod
        def setUpClass(cls):
            """Set up the environment before running 'all' command tests."""
            try:
                os.rename("file.json", "tmp")
            except IOError:
                pass
            FileStorage._FileStorage__objects = {}

        @classmethod
        def tearDownClass(cls):
            """Clean up the environment after running 'all' command tests."""
            try:
                os.remove("file.json")
            except IOError:
                pass
            try:
                os.rename("tmp", "file.json")
            except IOError:
                pass

        def test_all_command_with_nonexistent_class(self):
            """Test the 'all' command with a class that doesn't exist."""
            expected_message = "** class doesn't exist **"
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("all MyModel"))
                self.assertEqual(expected_message, output.getvalue().strip())

        def test_all_command_displaying_all_objects_space_notation(self):
            """Test the 'all' command displaying all objects using space notation."""
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
                self.assertFalse(HBNBCommand().onecmd("create User"))
                self.assertFalse(HBNBCommand().onecmd("create State"))
                self.assertFalse(HBNBCommand().onecmd("create Place"))
                self.assertFalse(HBNBCommand().onecmd("create City"))
                self.assertFalse(HBNBCommand().onecmd("create Amenity"))
                self.assertFalse(HBNBCommand().onecmd("create Review"))
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("all"))
                self.assertIn("BaseModel", output.getvalue().strip())
                self.assertIn("User", output.getvalue().strip())
                self.assertIn("State", output.getvalue().strip())
                self.assertIn("Place", output.getvalue().strip())
                self.assertIn("City", output.getvalue().strip())
                self.assertIn("Amenity", output.getvalue().strip())
                self.assertIn("Review", output.getvalue().strip())

        def test_all_command_displaying_all_objects_dot_notation(self):
            """Test the 'all' command displaying all objects using dot notation."""
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
                self.assertFalse(HBNBCommand().onecmd("create User"))
                self.assertFalse(HBNBCommand().onecmd("create State"))
                self.assertFalse(HBNBCommand().onecmd("create Place"))
                self.assertFalse(HBNBCommand().onecmd("create City"))
                self.assertFalse(HBNBCommand().onecmd("create Amenity"))
                self.assertFalse(HBNBCommand().onecmd("create Review"))
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(".all()"))
                self.assertIn("BaseModel", output.getvalue().strip())
                self.assertIn("User", output.getvalue().strip())
                self.assertIn("State", output.getvalue().strip())
                self.assertIn("Place", output.getvalue().strip())
                self.assertIn("City", output.getvalue().strip())
                self.assertIn("Amenity", output.getvalue().strip())
                self.assertIn("Review", output.getvalue().strip())

        def test_all_command_for_single_object_type_space_notation(self):
            """Test the 'all' command for a single object type using space notation."""
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
                self.assertFalse(HBNBCommand().onecmd("create User"))
                self.assertFalse(HBNBCommand().onecmd("create State"))
                self.assertFalse(HBNBCommand().onecmd("create City"))
                self.assertFalse(HBNBCommand().onecmd("create Amenity"))
                self.assertFalse(HBNBCommand().onecmd("create Place"))
                self.assertFalse(HBNBCommand().onecmd("create Review"))

            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("all BaseModel"))
                self.assertIn("BaseModel", output.getvalue().strip())
                self.assertNotIn("User", output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("all User"))
                self.assertIn("User", output.getvalue().strip())
                self.assertNotIn("BaseModel", output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("all State"))
                self.assertIn("State", output.getvalue().strip())
                self.assertNotIn("BaseModel", output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("all City"))
                self.assertIn("City", output.getvalue().strip())
                self.assertNotIn("BaseModel", output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("all Amenity"))
                self.assertIn("Amenity", output.getvalue().strip())
                self.assertNotIn("BaseModel", output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("all Place"))
                self.assertIn("Place", output.getvalue().strip())
                self.assertNotIn("BaseModel", output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("all Review"))
                self.assertIn("Review", output.getvalue().strip())
                self.assertNotIn("BaseModel", output.getvalue().strip())

    class TestHBNBCommandUpdate(unittest.TestCase):
        """Unit tests for the 'update' command in the AirBnB clone command interpreter."""

        @classmethod
        def setUpClass(cls):
            """Set up the environment before running 'update' command tests."""
            try:
                os.rename("file.json", "tmp")
            except IOError:
                pass
            FileStorage._FileStorage__objects = {}

        @classmethod
        def tearDownClass(cls):
            """Clean up the environment after running 'update' command tests."""
            try:
                os.remove("file.json")
            except IOError:
                pass
            try:
                os.rename("tmp", "file.json")
            except IOError:
                pass

        def test_update_command_without_class_name(self):
            """Test the 'update' command without specifying a class name."""
            expected_message = "** class name missing **"
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("update"))
                self.assertEqual(expected_message, output.getvalue().strip())

        def test_update_command_without_class_name_dot_notation(self):
            """Test the 'update' command without specifying a class name using dot notation."""
            expected_message = "** class name missing **"
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd(".update()"))
                self.assertEqual(expected_message, output.getvalue().strip())

    class TestHBNBCommandUpdateInvalidClass(unittest.TestCase):
        """Tests for the 'update' command with an invalid class name in the AirBnB clone command interpreter."""

        def test_update_command_with_nonexistent_class(self):
            """Test the 'update' command with a class that doesn't exist."""
            expected_message = "** class doesn't exist **"
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("update MyModel"))
                self.assertEqual(expected_message, output.getvalue().strip())

        def test_update_command_with_nonexistent_class_dot_notation(self):
            """Test the 'update' command with a class that doesn't exist using dot notation."""
            expected_message = "** class doesn't exist **"
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("MyModel.update()"))
                self.assertEqual(expected_message, output.getvalue().strip())

    class TestHBNBCommandUpdateMissingID(unittest.TestCase):
        """Tests for the 'update' command when the instance ID is missing in the AirBnB clone command interpreter."""

        def test_update_command_without_id_space_notation(self):
            """Test the 'update' command without providing an instance ID using space notation."""
            expected_message = "** instance id missing **"
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("update BaseModel"))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("update User"))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("update State"))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("update City"))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("update Amenity"))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("update Place"))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("update Review"))
                self.assertEqual(expected_message, output.getvalue().strip())

        def test_update_command_without_id_dot_notation(self):
            """Test the 'update' command without providing an instance ID using dot notation."""
            expected_message = "** instance id missing **"
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("BaseModel.update()"))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("User.update()"))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("State.update()"))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("City.update()"))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("Amenity.update()"))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("Place.update()"))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("Review.update()"))
                self.assertEqual(expected_message, output.getvalue().strip())

    class TestHBNBCommandUpdateInvalidID(unittest.TestCase):
        """Tests for the 'update' command with an invalid instance ID in the AirBnB clone command interpreter."""

        def test_update_command_with_invalid_id_space_notation(self):
            """Test the 'update' command with an invalid instance ID using space notation."""
            expected_message = "** no instance found **"
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("update BaseModel 1"))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("update User 1"))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("update State 1"))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("update City 1"))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("update Amenity 1"))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("update Place 1"))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("update Review 1"))
                self.assertEqual(expected_message, output.getvalue().strip())

        def test_update_command_with_invalid_id_dot_notation(self):
            """Test the 'update' command with an invalid instance ID using dot notation."""
            expected_message = "** no instance found **"
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("BaseModel.update(1)"))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("User.update(1)"))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("State.update(1)"))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("City.update(1)"))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("Amenity.update(1)"))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("Place.update(1)"))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("Review.update(1)"))
                self.assertEqual(expected_message, output.getvalue().strip())

        def test_update_without_attribute_name_using_space_notation(self):
            """Test updating an instance without providing an attribute name using space notation."""
            expected_message = "** attribute name missing **"
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
                instance_id = output.getvalue().strip()
                command = f"update BaseModel {instance_id}"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create User"))
                instance_id = output.getvalue().strip()
                command = f"update User {instance_id}"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create State"))
                instance_id = output.getvalue().strip()
                command = f"update State {instance_id}"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create City"))
                instance_id = output.getvalue().strip()
                command = f"update City {instance_id}"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create Amenity"))
                instance_id = output.getvalue().strip()
                command = f"update Amenity {instance_id}"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create Place"))
                instance_id = output.getvalue().strip()
                command = f"update Place {instance_id}"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create Review"))
                instance_id = output.getvalue().strip()
                command = f"update Review {instance_id}"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(expected_message, output.getvalue().strip())

        def test_update_without_attribute_name_using_dot_notation(self):
            """Test updating an instance without providing an attribute name using dot notation."""
            expected_message = "** attribute name missing **"
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
                instance_id = output.getvalue().strip()
                command = f"BaseModel.update({instance_id})"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create User"))
                instance_id = output.getvalue().strip()
                command = f"User.update({instance_id})"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create State"))
                instance_id = output.getvalue().strip()
                command = f"State.update({instance_id})"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create City"))
                instance_id = output.getvalue().strip()
                command = f"City.update({instance_id})"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create Amenity"))
                instance_id = output.getvalue().strip()
                command = f"Amenity.update({instance_id})"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create Place"))
                instance_id = output.getvalue().strip()
                command = f"Place.update({instance_id})"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create Review"))
                instance_id = output.getvalue().strip()
                command = f"Review.update({instance_id})"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(expected_message, output.getvalue().strip())

        def test_update_without_attribute_value_using_space_notation(self):
            """Test updating an instance without providing an attribute value using space notation."""
            expected_message = "** value missing **"
            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create BaseModel")
                instance_id = output.getvalue().strip()
                command = f"update BaseModel {instance_id} attr_name"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create User")
                instance_id = output.getvalue().strip()
                command = f"update User {instance_id} attr_name"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create State")
                instance_id = output.getvalue().strip()
                command = f"update State {instance_id} attr_name"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create City")
                instance_id = output.getvalue().strip()
                command = f"update City {instance_id} attr_name"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create Amenity")
                instance_id = output.getvalue().strip()
                command = f"update Amenity {instance_id} attr_name"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create Place")
                instance_id = output.getvalue().strip()
                command = f"update Place {instance_id} attr_name"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create Review")
                instance_id = output.getvalue().strip()
                command = f"update Review {instance_id} attr_name"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(expected_message, output.getvalue().strip())

        def test_update_without_attribute_value_using_dot_notation(self):
            """Test updating an instance without providing an attribute value using dot notation."""
            expected_message = "** value missing **"
            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create BaseModel")
                instance_id = output.getvalue().strip()
                command = f"BaseModel.update({instance_id}, attr_name)"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create User")
                instance_id = output.getvalue().strip()
                command = f"User.update({instance_id}, attr_name)"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create State")
                instance_id = output.getvalue().strip()
                command = f"State.update({instance_id}, attr_name)"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create City")
                instance_id = output.getvalue().strip()
                command = f"City.update({instance_id}, attr_name)"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create Amenity")
                instance_id = output.getvalue().strip()
                command = f"Amenity.update({instance_id}, attr_name)"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create Place")
                instance_id = output.getvalue().strip()
                command = f"Place.update({instance_id}, attr_name)"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(expected_message, output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create Review")
                instance_id = output.getvalue().strip()
                command = f"Review.update({instance_id}, attr_name)"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(expected_message, output.getvalue().strip())

        def test_update_with_valid_string_attribute_using_space_notation(self):
            """Test updating an instance with a valid string attribute using space notation."""
            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create BaseModel")
                instance_id = output.getvalue().strip()
            command = f"update BaseModel {instance_id} attr_name 'attr_value'"
            self.assertFalse(HBNBCommand().onecmd(command))
            instance_dict = storage.all()[f"BaseModel.{instance_id}"].__dict__
            self.assertEqual("attr_value", instance_dict["attr_name"])

            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create User")
                instance_id = output.getvalue().strip()
            command = f"update User {instance_id} attr_name 'attr_value'"
            self.assertFalse(HBNBCommand().onecmd(command))
            instance_dict = storage.all()[f"User.{instance_id}"].__dict__
            self.assertEqual("attr_value", instance_dict["attr_name"])

            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create State")
                instance_id = output.getvalue().strip()
            command = f"update State {instance_id} attr_name 'attr_value'"
            self.assertFalse(HBNBCommand().onecmd(command))
            instance_dict = storage.all()[f"State.{instance_id}"].__dict__
            self.assertEqual("attr_value", instance_dict["attr_name"])

            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create City")
                instance_id = output.getvalue().strip()
            command = f"update City {instance_id} attr_name 'attr_value'"
            self.assertFalse(HBNBCommand().onecmd(command))
            instance_dict = storage.all()[f"City.{instance_id}"].__dict__
            self.assertEqual("attr_value", instance_dict["attr_name"])

            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create Amenity")
                instance_id = output.getvalue().strip()
            command = f"update Amenity {instance_id} attr_name 'attr_value'"
            self.assertFalse(HBNBCommand().onecmd(command))
            instance_dict = storage.all()[f"Amenity.{instance_id}"].__dict__
            self.assertEqual("attr_value", instance_dict["attr_name"])

            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create Place")
                instance_id = output.getvalue().strip()
            command = f"update Place {instance_id} attr_name 'attr_value'"
            self.assertFalse(HBNBCommand().onecmd(command))
            instance_dict = storage.all()[f"Place.{instance_id}"].__dict__
            self.assertEqual("attr_value", instance_dict["attr_name"])

            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create Review")
                instance_id = output.getvalue().strip()
            command = f"update Review {instance_id} attr_name 'attr_value'"
            self.assertFalse(HBNBCommand().onecmd(command))
            instance_dict = storage.all()[f"Review.{instance_id}"].__dict__
            self.assertEqual("attr_value", instance_dict["attr_name"])

        def test_update_with_valid_string_attribute_using_dot_notation(self):
            """Test updating an instance with a valid string attribute using dot notation."""
            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create BaseModel")
                instance_id = output.getvalue().strip()
            command = f"BaseModel.update({instance_id}, attr_name, 'attr_value')"
            self.assertFalse(HBNBCommand().onecmd(command))
            instance_dict = storage.all()[f"BaseModel.{instance_id}"].__dict__
            self.assertEqual("attr_value", instance_dict["attr_name"])

            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create User")
                instance_id = output.getvalue().strip()
            command = f"User.update({instance_id}, attr_name, 'attr_value')"
            self.assertFalse(HBNBCommand().onecmd(command))
            instance_dict = storage.all()[f"User.{instance_id}"].__dict__
            self.assertEqual("attr_value", instance_dict["attr_name"])

            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create State")
                instance_id = output.getvalue().strip()
            command = f"State.update({instance_id}, attr_name, 'attr_value')"
            self.assertFalse(HBNBCommand().onecmd(command))
            instance_dict = storage.all()[f"State.{instance_id}"].__dict__
            self.assertEqual("attr_value", instance_dict["attr_name"])

            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create City")
                instance_id = output.getvalue().strip()
            command = f"City.update({instance_id}, attr_name, 'attr_value')"
            self.assertFalse(HBNBCommand().onecmd(command))
            instance_dict = storage.all()[f"City.{instance_id}"].__dict__
            self.assertEqual("attr_value", instance_dict["attr_name"])

            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create Amenity")
                instance_id = output.getvalue().strip()
            command = f"BaseModel.Amenity({instance_id}, attr_name, 'attr_value')"
            self.assertFalse(HBNBCommand().onecmd(command))
            instance_dict = storage.all()[f"Amenity.{instance_id}"].__dict__
            self.assertEqual("attr_value", instance_dict["attr_name"])

            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create Place")
                instance_id = output.getvalue().strip()
            command = f"Place.update({instance_id}, attr_name, 'attr_value')"
            self.assertFalse(HBNBCommand().onecmd(command))
            instance_dict = storage.all()[f"Place.{instance_id}"].__dict__
            self.assertEqual("attr_value", instance_dict["attr_name"])

            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create Review")
                instance_id = output.getvalue().strip()
            command = f"Review.update({instance_id}, attr_name, 'attr_value')"
            self.assertFalse(HBNBCommand().onecmd(command))
            instance_dict = storage.all()[f"Review.{instance_id}"].__dict__
            self.assertEqual("attr_value", instance_dict["attr_name"])

        def test_update_with_valid_integer_attribute_using_space_notation(self):
            """Test updating an instance with a valid integer attribute using space notation."""
            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create Place")
                instance_id = output.getvalue().strip()
            command = f"update Place {instance_id} max_guest 98"
            self.assertFalse(HBNBCommand().onecmd(command))
            instance_dict = storage.all()[f"Place.{instance_id}"].__dict__
            self.assertEqual(98, instance_dict["max_guest"])

        def test_update_with_valid_integer_attribute_using_dot_notation(self):
            """Test updating an instance with a valid integer attribute using dot notation."""
            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create Place")
                instance_id = output.getvalue().strip()
            command = f"Place.update({instance_id}, max_guest, 98)"
            self.assertFalse(HBNBCommand().onecmd(command))
            instance_dict = storage.all()[f"Place.{instance_id}"].__dict__
            self.assertEqual(98, instance_dict["max_guest"])

        def test_update_with_valid_float_attribute_using_space_notation(self):
            """Test updating an instance with a valid float attribute using space notation."""
            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create Place")
                instance_id = output.getvalue().strip()
            command = f"update Place {instance_id} latitude 7.2"
            self.assertFalse(HBNBCommand().onecmd(command))
            instance_dict = storage.all()[f"Place.{instance_id}"].__dict__
            self.assertEqual(7.2, instance_dict["latitude"])

        def test_update_with_valid_float_attribute_using_dot_notation(self):
            """Test updating an instance with a valid float attribute using dot notation."""
            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create Place")
                instance_id = output.getvalue().strip()
            command = f"Place.update({instance_id}, latitude, 7.2)"
            self.assertFalse(HBNBCommand().onecmd(command))
            instance_dict = storage.all()[f"Place.{instance_id}"].__dict__
            self.assertEqual(7.2, instance_dict["latitude"])

        def test_update_with_valid_dictionary_using_space_notation(self):
            """Test updating an instance with a valid dictionary using space notation."""
            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create BaseModel")
                instance_id = output.getvalue().strip()
            command = f"update BaseModel {instance_id} {{'attr_name': 'attr_value'}}"
            HBNBCommand().onecmd(command)
            instance_dict = storage.all()[f"BaseModel.{instance_id}"].__dict__
            self.assertEqual("attr_value", instance_dict["attr_name"])

            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create User")
                instance_id = output.getvalue().strip()
            command = f"update User {instance_id} {{'attr_name': 'attr_value'}}"
            HBNBCommand().onecmd(command)
            instance_dict = storage.all()[f"User.{instance_id}"].__dict__
            self.assertEqual("attr_value", instance_dict["attr_name"])

            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create State")
                instance_id = output.getvalue().strip()
            command = f"update State {instance_id} {{'attr_name': 'attr_value'}}"
            HBNBCommand().onecmd(command)
            instance_dict = storage.all()[f"State.{instance_id}"].__dict__
            self.assertEqual("attr_value", instance_dict["attr_name"])

            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create City")
                instance_id = output.getvalue().strip()
            command = f"update City {instance_id} {{'attr_name': 'attr_value'}}"
            HBNBCommand().onecmd(command)
            instance_dict = storage.all()[f"City.{instance_id}"].__dict__
            self.assertEqual("attr_value", instance_dict["attr_name"])

            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create Amenity")
                instance_id = output.getvalue().strip()
            command = f"update Amenity {instance_id} {{'attr_name': 'attr_value'}}"
            HBNBCommand().onecmd(command)
            instance_dict = storage.all()[f"Amenity.{instance_id}"].__dict__
            self.assertEqual("attr_value", instance_dict["attr_name"])

            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create Place")
                instance_id = output.getvalue().strip()
            command = f"update Place {instance_id} {{'attr_name': 'attr_value'}}"
            HBNBCommand().onecmd(command)
            instance_dict = storage.all()[f"Place.{instance_id}"].__dict__
            self.assertEqual("attr_value", instance_dict["attr_name"])

            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create Review")
                instance_id = output.getvalue().strip()
            command = f"update Review {instance_id} {{'attr_name': 'attr_value'}}"
            HBNBCommand().onecmd(command)
            instance_dict = storage.all()[f"Review.{instance_id}"].__dict__
            self.assertEqual("attr_value", instance_dict["attr_name"])

        def test_update_with_valid_dictionary_using_dot_notation(self):
            """Test updating an instance with a valid dictionary using dot notation."""
            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create BaseModel")
                instance_id = output.getvalue().strip()
            command = f"BaseModel.update({instance_id}, {{'attr_name': 'attr_value'}})"
            HBNBCommand().onecmd(command)
            instance_dict = storage.all()[f"BaseModel.{instance_id}"].__dict__
            self.assertEqual("attr_value", instance_dict["attr_name"])

            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create User")
                instance_id = output.getvalue().strip()
            command = f"User.update({instance_id}, {{'attr_name': 'attr_value'}})"
            HBNBCommand().onecmd(command)
            instance_dict = storage.all()[f"User.{instance_id}"].__dict__
            self.assertEqual("attr_value", instance_dict["attr_name"])

            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create State")
                instance_id = output.getvalue().strip()
            command = f"State.update({instance_id}, {{'attr_name': 'attr_value'}})"
            HBNBCommand().onecmd(command)
            instance_dict = storage.all()[f"State.{instance_id}"].__dict__
            self.assertEqual("attr_value", instance_dict["attr_name"])

            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create City")
                instance_id = output.getvalue().strip()
            command = f"City.update({instance_id}, {{'attr_name': 'attr_value'}})"
            HBNBCommand().onecmd(command)
            instance_dict = storage.all()[f"City.{instance_id}"].__dict__
            self.assertEqual("attr_value", instance_dict["attr_name"])

            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create Amenity")
                instance_id = output.getvalue().strip()
            command = f"Amenity.update({instance_id}, {{'attr_name': 'attr_value'}})"
            HBNBCommand().onecmd(command)
            instance_dict = storage.all()[f"Amenity.{instance_id}"].__dict__
            self.assertEqual("attr_value", instance_dict["attr_name"])

            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create Place")
                instance_id = output.getvalue().strip()
            command = f"Place.update({instance_id}, {{'attr_name': 'attr_value'}})"
            HBNBCommand().onecmd(command)
            instance_dict = storage.all()[f"Place.{instance_id}"].__dict__
            self.assertEqual("attr_value", instance_dict["attr_name"])

            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create Review")
                instance_id = output.getvalue().strip()
            command = f"Review.update({instance_id}, {{'attr_name': 'attr_value'}})"
            HBNBCommand().onecmd(command)
            instance_dict = storage.all()[f"Review.{instance_id}"].__dict__
            self.assertEqual("attr_value", instance_dict["attr_name"])

        def test_update_with_valid_dictionary_containing_integer_using_space_notation(self):
            """Test updating an instance with a valid dictionary containing an integer using space notation."""
            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create Place")
                instance_id = output.getvalue().strip()
            command = f"update Place {instance_id} {{'max_guest': 98}}"
            HBNBCommand().onecmd(command)
            instance_dict = storage.all()[f"Place.{instance_id}"].__dict__
            self.assertEqual(98, instance_dict["max_guest"])

        def test_update_with_valid_dictionary_containing_integer_using_dot_notation(self):
            """Test updating an instance with a valid dictionary containing an integer using dot notation."""
            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create Place")
                instance_id = output.getvalue().strip()
            command = f"Place.update({instance_id}, {{'max_guest': 98}})"
            HBNBCommand().onecmd(command)
            instance_dict = storage.all()[f"Place.{instance_id}"].__dict__
            self.assertEqual(98, instance_dict["max_guest"])

        def test_update_with_valid_dictionary_containing_float_using_space_notation(self):
            """Test updating an instance with a valid dictionary containing a float using space notation."""
            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create Place")
                instance_id = output.getvalue().strip()
            command = f"update Place {instance_id} {{'latitude': 9.8}}"
            HBNBCommand().onecmd(command)
            instance_dict = storage.all()[f"Place.{instance_id}"].__dict__
            self.assertEqual(9.8, instance_dict["latitude"])

        def test_update_with_valid_dictionary_containing_float_using_dot_notation(self):
            """Test updating an instance with a valid dictionary containing a float using dot notation."""
            with patch("sys.stdout", new=StringIO()) as output:
                HBNBCommand().onecmd("create Place")
                instance_id = output.getvalue().strip()
            command = f"Place.update({instance_id}, {{'latitude': 9.8}})"
            HBNBCommand().onecmd(command)
            instance_dict = storage.all()[f"Place.{instance_id}"].__dict__
            self.assertEqual(9.8, instance_dict["latitude"])

    class TestHBNBCommandCount(unittest.TestCase):
        """Unit tests for the 'count' method in the AirBnB clone command interpreter."""

        @classmethod
        def setUpClass(cls):
            """Prepare the environment before running the 'count' method tests."""
            try:
                os.rename("file.json", "tmp")
            except IOError:
                pass
            FileStorage._FileStorage__objects = {}

        @classmethod
        def tearDownClass(cls):
            """Clean up the environment after running the 'count' method tests."""
            try:
                os.remove("file.json")
            except IOError:
                pass
            try:
                os.rename("tmp", "file.json")
            except IOError:
                pass

        def test_count_method_with_invalid_class(self):
            """Test the 'count' method with a class that doesn't exist."""
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("MyModel.count()"))
                self.assertEqual("0", output.getvalue().strip())

        def test_count_method_with_objects(self):
            """Test the 'count' method with various object types."""
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("BaseModel.count()"))
                self.assertEqual("1", output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create User"))
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("User.count()"))
                self.assertEqual("1", output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("State BaseModel"))
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("State.count()"))
                self.assertEqual("1", output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create City"))
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("City.count()"))
                self.assertEqual("1", output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("Amenity.count()"))
                self.assertEqual("1", output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create Place"))
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("Place.count()"))
                self.assertEqual("1", output.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("create Review"))
            with patch("sys.stdout", new=StringIO()) as output:
                self.assertFalse(HBNBCommand().onecmd("Review.count()"))
                self.assertEqual("1", output.getvalue().strip())

    if __name__ == "__main__":
        unittest.main()

