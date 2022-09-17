#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Relationship, Base
from sqlalchemy import Column, String, ForeignKey
from os import getenv


class City(BaseModel):
    """ The city class, contains state ID and name """
    if storage_type == 'db':
        __tablename__ = 'cities'

        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        places = Relationship('Place', cascade='all, delete', backref='cities')
    else:
        state_id = ""
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes"""
        super().__init__(*args, **kwargs)
