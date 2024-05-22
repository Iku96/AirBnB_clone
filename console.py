#!/usr/bin/python3
"""This module sets up the AirBnB clone console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def extract_arguments(argument):
    """Extracts arguments from the command line input."""
    curly_braces_content = re.search(r"\{(.*?)\}", argument)
    square_brackets_content = re.search(r"\[(.*?)\]", argument)
    if not curly_braces_content:
        if not square_brackets_content:
            return [item.strip(",") for item in split(argument)]
        else:
            pre_bracket_args = split(argument[:square_brackets_content.span()[0]])
            return [item.strip(",") for item in pre_bracket_args] + [square_brackets_content.group()]
    else:
        pre_curly_args = split(argument[:curly_braces_content.span()[0]])
        return [item.strip(",") for item in pre_curly_args] + [curly_braces_content.group()]


class HBNBCommand(cmd.Cmd):
    """Represents the command interpreter for HBNB clone.

    Attributes:
        prompt (str): The command line prompt.
    """

    prompt = "(hbnb) "
    __models = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Ignores empty lines."""
        pass

    def default(self, line):
        """Handles unrecognized commands."""
        commands_dict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        dot_search = re.search(r"\.", line)
        if dot_search:
            args = [line[:dot_search.span()[0]], line[dot_search.span()[1]:]]
            parentheses_search = re.search(r"\((.*?)\)", args[1])
            if parentheses_search:
                command = [args[1][:parentheses_search.span()[0]], parentheses_search.group()[1:-1]]
                if command[0] in commands_dict:
                    call = "{} {}".format(args[0], command[1])
                    return commands_dict[command[0]](call)
        print("*** Unrecognized command: {}".format(line))
        return False

    def do_quit(self, line):
        """Exits the console."""
        return True

    def do_EOF(self, line):
        """Ends the console session."""
        print("")
        return True

    def do_create(self, line):
        """Creates a new instance of a specified model."""
        args = extract_arguments(line)
        if not args:
            print("** Missing model name **")
        elif args[0] not in HBNBCommand.__models:
            print("** Model does not exist **")
        else:
            print(eval(args[0])().id)
            storage.save()

    def do_show(self, line):
        """Displays the details of a specific model instance."""
        args = extract_arguments(line)
        all_objects = storage.all()
        if not args:
            print("** Missing model name **")
        elif args[0] not in HBNBCommand.__models:
            print("** Model does not exist **")
        elif len(args) == 1:
            print("** Missing instance ID **")
        elif "{}.{}".format(args[0], args[1]) not in all_objects:
            print("** Instance not found **")
        else:
            print(all_objects["{}.{}".format(args[0], args[1])])

    def do_destroy(self, line):
        """Deletes a specific model instance."""
        args = extract_arguments(line)
        all_objects = storage.all()
        if not args:
            print("** Missing model name **")
        elif args[0] not in HBNBCommand.__models:
            print("** Model does not exist **")
        elif len(args) == 1:
            print("** Missing instance ID **")
        elif "{}.{}".format(args[0], args[1]) not in all_objects.keys():
            print("** Instance not found **")
        else:
            del all_objects["{}.{}".format(args[0], args[1])]
            storage.save()

    def do_all(self, line):
        """Displays all instances of a specified model or all instantiated objects."""
        args = extract_arguments(line)
        if args and args[0] not in HBNBCommand.__models:
            print("** Model does not exist **")
        else:
            object_list = []
            for obj in storage.all().values():
                if args and args[0] == obj.__class__.__name__:
                    object_list.append(obj.__str__())
                elif not args:
                    object_list.append(obj.__str__())
            print(object_list)

    def do_count(self, line):
        """Counts the number of instances of a specified model."""
        args = extract_arguments(line)
        count = sum(1 for obj in storage.all().values() if args[0] == obj.__class__.__name__)
        print(count)

    def do_update(self, line):
        """Updates an instance based on its ID with new attribute values."""
        args = extract_arguments(line)
        all_objects = storage.all()

        if not args:
            print("** Missing model name **")
            return False
        if args[0] not in HBNBCommand.__models:
            print("** Model does not exist **")
            return False
        if len(args) == 1:
            print("** Missing instance ID **")
            return False
        if "{}.{}".format(args[0], args[1]) not in all_objects.keys():
            print("** Instance not found **")
            return False
        if len(args) == 2:
            print("** Missing attribute name **")
            return False
        if len(args) == 3:
            try:
                assert type(eval(args[2])) != dict
            except (NameError, AssertionError):
                print("** Missing value **")
                return False

        if len(args) == 4:
            obj = all_objects["{}.{}".format(args[0], args[1])]
            if args[2] in obj.__class__.__dict__:
                valtype = type(obj.__class__.__dict__[args[2]])
                obj.__dict__[args[2]] = valtype(args[3])
            else:
                obj.__dict__[args[2]] = args[3]
        elif isinstance(eval(args[2]), dict):
            obj = all_objects["{}.{}".format(args[0], args[1])]
            for key, value in eval(args[2]).items():
                if (key in obj.__class__.__dict__ and
                        isinstance(obj.__class__.__dict__[key], (str, int, float))):
                    valtype = type(obj.__class__.__dict__[key])
                    obj.__dict__[key] = valtype(value)
                else:
                    obj.__dict__[key] = value
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
