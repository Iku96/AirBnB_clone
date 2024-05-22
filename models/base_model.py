#!/usr/bin/python3
"""Module to establish the BaseModel class."""
import models
from uuid import uuid4
from datetime import datetime

class BaseModel:
    """Defines the base model for the AirBnB Clone project."""

    def __init__(self, *args, **kwargs):
        """Initializes a new instance of BaseModel.

        Args:
            *args (unused): Variable length argument list.
            **kwargs (dict): Key/value pairs of properties.
        """
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if kwargs:
            for key, value in kwargs.items():
                if key in ("created_at", "updated_at"):
                    self.__dict__[key] = datetime.strptime(value, time_format)
                else:
                    self.__dict__[key] = value
        else:
            models.storage.new(self)

    def save(self):
        """Records the current time as updated_at and saves to storage."""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Converts the BaseModel instance into a dictionary.

        This includes the special key '__class__' to note the object's class name.
        """
        dict_representation = self.__dict__.copy()
        dict_representation["created_at"] = self.created_at.isoformat()
        dict_representation["updated_at"] = self.updated_at.isoformat()
        dict_representation["__class__"] = type(self).__name__
        return dict_representation

    def __str__(self):
        """Generates a string representation of the BaseModel instance."""
        class_name = type(self).__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)
