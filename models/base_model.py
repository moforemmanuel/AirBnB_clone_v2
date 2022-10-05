#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

import models

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    # __tablename__ = 'BaseModel'

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        id = str(uuid.uuid4())
        created_at = datetime.now()
        updated_at = datetime.now()
        str_time = "%Y-%m-%dT%H:%M:%S.%f"
        if not kwargs:
            from models import storage
            self.id = id
            self.created_at = created_at
            self.updated_at = updated_at
            # storage.new(self)

        elif kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

        else:
            try:
                kwargs['updated_at'] = datetime.fromisoformat(
                                        kwargs['updated_at'])
                kwargs['created_at'] = datetime.fromisoformat(
                                        kwargs['created_at'])
                self.__dict__.update(kwargs)
            except KeyError:
                self.id = str(uuid.uuid4())
                kwargs['created_at'] = datetime.now()
                kwargs['updated_at'] = datetime.now()
                self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in dictionary.keys():
            # use del instead of pop, don't leak mem
            del dictionary['_sa_instance_state']
        return dictionary

    def delete(self):
        """ Delete current instance from storage """
        models.storage.delete(self)

