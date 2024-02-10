#!/usr/bin/python3
""" State Module for DBStorage engine"""
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from models.user import User
from models.profile import Profile
from models.projects import Project
import models

classes = {"User": User, "Profile": Profile, "Project": Project}


class DBStorage:
    """This class manages storage of hbnb models in MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            os.environ.get("PORTOGOLIO_MYSQL_USER"),
            os.environ.get("PORTOGOLIO__MYSQL_PWD"),
            os.environ.get("PORTOGOLIO__MYSQL_HOST", default="localhost"),
            os.environ.get("PORTOGOLIO__MYSQL_DB")), pool_pre_ping=True)

    def all(self, cls=None):
        """Returns a dictionary of objects of one type of cls"""
        results_dict = {}

        if cls:
            results = self.__session.query(cls).all()
            for obj in results:
                results_dict["{}.{}".format(cls.__name__, obj.id)] = obj
        else:
            cls = [User, Profile, Project]
            for c in cls:
                results = self.__session.query(c).all()

                for obj in results:
                    results_dict["{}.{}".format(
                        type(obj).__name__, obj.id)] = obj
        return results_dict

    def new(self, obj):
        """Adds new object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete an object from the current database session"""
        if obj:
            self.__session.delete(obj)
            print("DELETE")

    def reload(self):
        """Creates all tables in the session in the database """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """call remove on the private session attribute self.__session"""
        self.__session.close()

    def qurery_by_email(self, cls, email):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        result = self.__session.query(User).filter_by(email=email).first()
        return result or None

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None

    def get_by_fk(self, cls, fk_id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.user_id == fk_id):
                return value
        return None