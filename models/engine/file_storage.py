#!/usr/bin/python3
"""FileStorage class setup."""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

class FileStorage:
    """Class for saving and loading objects.

    Parts:
        __file_path (str): File to keep objects in.
        __objects (dict): All objects made.
    """
    __file_path = "file.json"  # Where to save objects
    __objects = {}  # Holds all created objects

    def all(self):
        """Give back all objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Add new object with its key."""
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """Turn objects into JSON and save."""
        with open(FileStorage.__file_path, 'w') as f:
            json.dump({k: v.to_dict() for k, v in FileStorage.__objects.items()}, f)

    def reload(self):
        """Load objects from JSON file if it's there."""
        try:
            with open(FileStorage.__file_path) as f:
                for obj in json.load(f).values():
                    name = obj['__class__']
                    del obj['__class__']
                    self.new(eval(name)(**obj))
        except FileNotFoundError:
            pass
