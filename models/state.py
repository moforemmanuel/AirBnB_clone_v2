#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv

storage_type = getenv("HBNB_TYPE_STORAGE")


class State(BaseModel, Base):
    """ State class """
    # name = ""
    __tablename__ = 'states'
    if storage_type == 'db':
        name = Column(String(60), nullable=False)
        # id = Column(String(60), primary_key=True, nullable=False)
        # children = relationship("City")
        cities = relationship("City", backref="state", cascade="all, delete-orphan")
    else:
        name = ""

    if storage_type != 'db':
        @property
        def cities(self):
            """ get list of city instances with state_id
                equals current state.id
             """
            list_cities = []
            all_cities = models.storage.all(City)
            for key, city_obj in all_cities.items():
                if city_obj.state_id == self.id:
                    list_cities.append(city_obj)
            return list_cities
