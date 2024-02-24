#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, ForeignKey


class Profile(BaseModel, Base):
    """This class defines a user by attributes"""

    __tablename__ = "profiles"
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)