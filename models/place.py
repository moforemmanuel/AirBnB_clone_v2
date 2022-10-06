#!/usr/bin/python3
""" Place Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from models.review import Review
# from models.amenity import Amenity
from os import getenv
from sqlalchemy import Column, Table, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship


storage_type = getenv('HBNB_TYPE_STORAGE')

if storage_type == 'db':
    metadata = Base.metadata
    place_amenity = Table(
        'place_amenity',
        metadata,
        Column('place_id',
               String(60),
               ForeignKey('places.id'),
               # primary_key=True,
               nullable=False),
        Column('amenity_id',
               String(60),
               ForeignKey('amenities.id'),
               # primary_key=True,
               nullable=False)
    )


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
        amenities = relationship(
            'Amenity',
            secondary=place_amenity,
            back_populates='place_amenities',
            viewonly=False
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

        @property
        def amenities(self):
            """
            returns list of Amenities
            with amenity_id == amenity.id
            and linked to the place
            """
            # list_amenities = []
            # # place_amenities_objs = models.storage.all(Amenity)
            # # for key, amen_obj in place_amenities_objs.items():
            # #     if amen_obj.id in self.amenity_ids:
            # #         list_amenities.append(amen_obj)
            #
            # return list_amenities
            amenity_objs = []
            for amenity_id in self.amenity_ids:
                key = 'Amenity.' + amenity_id
                if key in models.storage.all():
                    amenity_objs.append(models.storage.all()[key])

            return amenity_objs

        @amenities.setter
        def amenities(self, amenity):
            """
            adds Amenity.id to amenity_ids
            """
            # def append(amenity):
            #     if isinstance(amenity, models.__init__.classes['Amenity']):
            #         self.amenity_ids.append(amenity.id)
            if isinstance(amenity, models.__init__.classes['Amenity']):
                self.amenity_ids.append(amenity.id)
