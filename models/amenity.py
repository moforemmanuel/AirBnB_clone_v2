#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Float, ForeignKey


storage_type = getenv('HBNB_TYPE_STORAGE')


class Amenity(BaseModel, Base):
    """
    Amenity model
    """

    __tablename__ = 'amenities'
    if storage_type == 'db':
        from models.place import place_amenity
        name = Column(String(128), nullable=False)
        place_amenities = relationship(
            'Place',
            secondary=place_amenity,
            back_populates='amenities'
        )

    else:
        name = ""
