#!/usr/bin/python3
"""This module instantiates an object of class DBStorage"""
from .db.db_storage import DBStorage

storage = DBStorage()
storage.reload()