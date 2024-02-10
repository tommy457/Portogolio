#!/usr/bin/python3
"""This module defines a class Tag"""
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column


class Tag(BaseModel, Base):
    """This class defines a user by attributes"""
    __tablename__ = 'tags'
    name = Column(String(20), nullable=False, unique=True)