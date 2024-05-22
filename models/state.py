#!/usr/bin/python3
"""State class definition."""

from models.base_model import BaseModel

class State(BaseModel):
    """This class is for states.

    Parts:
        name (str): The state's name.
    """

    name = ""  # Name of the state
