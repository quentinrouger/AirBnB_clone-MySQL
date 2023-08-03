#!/usr/bin/python3
"""
File to manage the database
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base

class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """Create a new instance of DBStorage"""
        # MySQL user, password, host, and database from environment variables
        user = os.environ.get('HBNB_MYSQL_USER')
        pwd = os.environ.get('HBNB_MYSQL_PWD')
        host = os.environ.get('HBNB_MYSQL_HOST', 'localhost')
        db_name = os.environ.get('HBNB_MYSQL_DB')

        # Construct the database URI
        db_uri = 'mysql+mysqldb://{}:{}@{}:3306/{}'.format(user, pwd, host, db_name)

        # Create the engine and add pool_pre_ping=True option
        self.__engine = create_engine(db_uri, pool_pre_ping=True)
        
    def reload(self):
        """Create all tables in the database and initialize a new session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def save(self):
        """Commit all changes of the current session to the database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current session if not None"""
        if obj:
            self.__session.delete(obj)

    def all(self, cls=None):
        """Query all objects of a certain class or all classes"""
        from models import classes

        result = {}
        if cls:
            query_result = self.__session.query(classes[cls]).all()
            for obj in query_result:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                result[key] = obj
        else:
            for cls in classes.values():
                query_result = self.__session.query(cls).all()
                for obj in query_result:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    result[key] = obj
        return result

    def new(self, obj):
        """Add obj to the current session"""
        self.__session.add(obj)

    def close(self):
        """Remove the session"""
        self.__session.remove()
