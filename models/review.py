#!/usr/bin/python3
"""This file has the Review class."""

from models.base_model import BaseModel

class Review(BaseModel):
    """This class is for reviews.

    Parts:
        place_id (str): ID for the Place.
        user_id (str): ID for the User.
        text (str): The review words.
    """

    place_id = ""  # ID for the place being talked about
    user_id = ""   # ID for the person who wrote the review
    text = ""      # What the person said in the review
