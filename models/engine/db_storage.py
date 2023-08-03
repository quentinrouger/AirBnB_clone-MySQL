#!/usr/bin/python3
"""
This script defines the DBStorage engine class.
"""

import json
from os import getenv
from models.base_model import Base, BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, scoped_session, sessionmaker



class DBStorage:
    """
    Represents a database storage engine.

    Attributes:
        __engine (sqlalchemy.Engine): The SQLAlchemy engine.
        __session (sqlalchemy.Session): The SQLAlchemy session.
    """

    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes a new DBStorage instance.
        """
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".
            format(getenv("HBNB_MYSQL_USER"),
                   getenv("HBNB_MYSQL_PWD"),
                   getenv("HBNB_MYSQL_HOST"),
                   getenv("HBNB_MYSQL_DB")),
            pool_pre_ping=True
        )
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Queries the current database session
        for all objects of the given class.

        If cls is None, queries all types of objects.

        Return:
            A dictionary of queried classes
            in the format <class name>.<obj id> = obj.
        """
        if cls is None:
            objs = (self.__session.query(State).all() +
                    self.__session.query(City).all() +
                    self.__session.query(User).all() +
                    self.__session.query(Place).all() +
                    self.__session.query(Review).all() +
                    self.__session.query(Amenity).all())
        else:
            if isinstance(cls, str):
                cls = eval(cls)
            objs = self.__session.query(cls).all()

        return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}

    def new(self, obj):
        """
        Adds obj to the current database session.
        """
        self.__session.add(obj)

    def save(self):
        """
        Commits all changes to the current database session.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes obj from the current database session.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Deserialize the JSON file __file_path to __objects, if it exists.
        """
        try:
            with open(self.__file_path, "r", encoding="utf-8") as file:
                try:
                    loaded_objects = json.load(file)
                    for key, value in loaded_objects.items():
                        class_name = value["__class__"]
                        del value["__class__"]
                        self.new(eval(class_name)(**value))
                except json.JSONDecodeError:
                    # JSON file is empty or corrupted
                    pass
        except FileNotFoundError:
            pass


    def close(self):
        """
        Closes the working SQLAlchemy session.
        """
        self.__session.close()
