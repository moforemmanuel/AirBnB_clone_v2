#!/usr/bin/python3

import unittest
import models
from models.base_model import BaseModel, Base
from models.user import User
from models.review import Review
from models.amenity import Amenity
from models.state import State
from models.place import Place
from models.city import City
import os
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 "only testing db storage")
class TestDBStorage(unittest.TestCase):
    """
    Test for DBS
    """

    def test_state(self):
        """ test state """
        state = State(name=" NW")
        if state.id in models.storage.all():
            self.assertTrue(state.name, 'NW')

if __name__ == '__main__':
    unittest.main()
