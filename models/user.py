#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, Table, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from models.tags import Tag


user_tag = Table('user_tag', Base.metadata,
                          Column('user_id', String(60),
                                 ForeignKey('users.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True),
                          Column('tag_id', String(60),
                                 ForeignKey('tags.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True))


class User(BaseModel, Base, UserMixin):
    """This class defines a user by attributes"""
    __tablename__ = 'users'
    username = Column(String(128), unique=True, nullable=False)
    role = Column(String(32), nullable=False)
    country = Column(String(20), nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    github = Column(String(128), unique=True, nullable=False)
    linkedin = Column(String(128), unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    profile_pic = Column(String(20), nullable=False, default='default.png')
    projects = relationship("Project", backref="user", cascade="all, delete")
    profile = relationship("Profile", backref="user", cascade="all, delete")
    tags = relationship("Tag", secondary=user_tag, viewonly=False)
    comments = relationship("Comment", backref="user", cascade="all, delete")