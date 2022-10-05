#!/usr/bin/python3
""" Place Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from models.review import Review
from os import getenv
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship


storage_type = getenv('HBNB_TYPE_STORAGE')


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

    if storage_type == 'db':
        city_id = Column(
            String(60),
            ForeignKey('cities.id'),
            nullable=False
        )
        user_id = Column(
            String(60),
            ForeignKey('users.id'),
            nullable=False
        )
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship(
            'Review',
            backref='place',
            cascade='all, delete-orphan'
        )

    else:
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

    if storage_type != 'db':
        @property
        def reviews(self):
            """
            returns list of Review instances with place_id = place.id
            """
            list_reviews = []
            place_reviews = models.storage.all(Review)
            for key, rev_obj in place_reviews.items():
                if rev_obj.place_id == self.id:
                    list_reviews.append(rev_obj)

            return list_reviews

