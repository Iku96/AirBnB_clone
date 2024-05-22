#!/usr/bin/python3
"""Module that introduces the Place class."""
from models.base_model import BaseModel

class Place(BaseModel):
    """Describes the characteristics of a lodging place.

    Attributes:
        city_id (str): Identifier for the city where the place is located.
        user_id (str): Identifier for the user who owns the place.
        name (str): Title of the lodging place.
        description (str): Detailed description of the place.
        number_rooms (int): Count of rooms available in the place.
        number_bathrooms (int): Count of bathrooms available in the place.
        max_guest (int): Maximum occupancy of the place.
        price_by_night (int): Cost per night to stay at the place.
        latitude (float): Geographical latitude of the place.
        longitude (float): Geographical longitude of the place.
        amenity_ids (list): Collection of Amenity identifiers associated with the place.
    """

    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
