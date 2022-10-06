#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

import models

Base = declarative_base()
date_format = "%Y-%m-%dT%H:%M:%S.%f"


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
        if kwargs:
            # assign dict of attribs to inst
            if kwargs.get('created_at'):
                kwargs['created_at'] = datetime.fromisoformat(
                    kwargs['created_at'])
                # or use datetime.strptime(kwargs['created_at'], date_formate)
            else:
                kwargs['created_at'] = datetime.utcnow()  # assign current time

            if kwargs.get('updated_at'):
                kwargs['updated_at'] = datetime.fromisoformat(
                    kwargs['updated_at'])
            else:
                kwargs['updated_at'] = datetime.utcnow()  # assign current time

            if not kwargs.get('id'):
                self.id = str(uuid.uuid4())

            for key, value in kwargs.items():
                if "__class__" not in key:
                    setattr(self, key, value)

        else:
            from models import storage
            self.id = id
            self.created_at = created_at
            self.updated_at = updated_at
            # storage.new(self)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        # print('creating')
        models.storage.new(self)
        # print('saving')
        models.storage.save()
        # print('commited')

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
