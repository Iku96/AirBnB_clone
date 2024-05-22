#!/usr/bin/python3
"""User class file."""

from models.base_model import BaseModel

class User(BaseModel):
    """Class for user info.

    Parts:
        email (str): User's email.
        password (str): User's secret code.
        first_name (str): User's given name.
        last_name (str): User's family name.
    """

    email = ""       # Email address
    password = ""    # Secret code for account
    first_name = ""  # Given name
    last_name = ""   # Family name
