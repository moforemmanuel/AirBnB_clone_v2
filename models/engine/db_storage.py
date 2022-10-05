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
socket = '?unix_socket=/opt/lampp/var/mysql/mysql.sock'


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
        # print('listing')
        # print(cls)
        cls_objs = {}
        # print(cls is None)

        if not cls:
            # print('no cls is present')
            for class_class in [State, City, User, Place]:
                for obj in self.__session.query(class_class).all():
                    key = f"{class_class.__name__}.{obj.id}"
                    val = obj
                    cls_objs[key] = val
            # print('result-no-cls: ', cls_objs, end='\n\n')

        else:
            # print('cls present: ', cls)
            # cls_dict = {}
            # keys = self.__objects.keys()
            if type(cls) is not str:
                cls = cls.__name__
            for obj in self.__session.query(classes[cls]).all():
                # print('objet: ', obj)
                key = f"{obj.__class__.__name__}.{obj.id}"
                value = obj
                cls_objs[key] = value

            # print('result-cls:', cls_objs, end='\n\n')

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
