#!/usr/bin/python3
"""Module for City class definition."""
from models.base_model import BaseModel

class City(BaseModel):
    """Defines the attributes of a city.

    Attributes:
        state_id (str): Identifier for the state.
        name (str): The official name of the city.
    """

    state_id = ""
    name = ""
