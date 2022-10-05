#!/usr/bin/python3
""" DB Storage for AirBnB """
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

database = getenv("HBNB_MYSQL_DB")
user = getenv("HBNB_MYSQL_USER")
host = getenv("HBNB_MYSQL_HOST")
password = getenv("HBNB_MYSQL_PWD")
hbnb_env = getenv("HBNB_ENV")


classes = {"State": State, "City": City, "User": User,
           "Place": Place, "Review": Review, "Amenity": Amenity}


class DBStorage:
    """ class declaration for DBStorage """
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, password, host, database),
                                      pool_pre_ping=True)

        if hbnb_env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        retrieve all instances of cls
        """
        cls_objs = {}
        if cls:
            if isinstance(cls, str) and cls in classes:
                for obj in self.__session.query(classes[cls]).all():
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    value = obj
                    cls_objs[key] = value

            elif cls.__name__ in classes:
                for obj in self.__session.query(cls).all():
                    key = str(obj.__class__.__name__) + "." + str(obj.id)
                    val = obj
                    cls_objs[key] = val

            else:
                for name, _class in classes.items():
                    for obj in self.__session.query(_class).all():
                        key = f"{_class.__name__}.{obj.id}"
                        val = obj
                        cls_objs[key] = val
            return cls_objs

    def new(self, obj):
        """
        add obj to current db session
        """
        self.__session.add(obj)

    def save(self):
        """
        commit all changes to db session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        delete from curent db session obj if not none
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        create all tables in db and create current
        db session
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False
        )
        Session = scoped_session(session_factory)
        self.__session = Session()
