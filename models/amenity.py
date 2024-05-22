#!/usr/bin/python3
"""Establishes the Amenity class."""
from models.base_model import BaseModel

class Amenity(BaseModel):
    """Defines an accommodation feature.

    Attributes:
        name (str): The designation of the feature.
    """

    name = ""
