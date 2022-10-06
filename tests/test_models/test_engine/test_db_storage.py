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
        if state.id in models.storage.all(State):
            self.assertTrue(state.name, 'NW')

    def test_city(self):
        """ test city """
        city = City(name='Bamenda')
        if city.id in models.storage.all(City):
            self.assertTrue(city.name, 'Bamenda')

    def test_place(self):
        """ test place """
        place = Place(name='Nkwen', number_rooms=500)
        if place.id in models.storage.all(Place):
            self.assertTrue(place.name, 'Nkwen')
            self.assertTrue(place.number_rooms, 500)

    def test_user(self):
        """ test user """
        user = User(name='Mofor')
        if user.id in models.storage.all(User):
            self.assertTrue(user.name, 'Mofor')

    def test_amenity(self):
        """ test amenity """
        amen = Amenity(name='Bar')
        if amen.id in models.storage.all(Amenity):
            self.assertTrue(amen.name, 'Bar')

    def test_review(self):
        """ test review """
        review = Review(text='Bamenda is love')
        if review.id in models.storage.all(Review):
            self.assertTrue(review.name, 'Bamenda is love')

    def tearDown(self) -> None:
        self.session.close()
        self.session.rollback()


if __name__ == '__main__':
    unittest.main()
