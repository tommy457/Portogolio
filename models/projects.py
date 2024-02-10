#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import String, Column, Text, ForeignKey, Table, JSON
from models.tags import Tag


project_tag = Table(
                     'project_tag',
                     Base.metadata,
                     Column('project_tag', String(60),
                            ForeignKey('projects.id', onupdate='CASCADE',
                                       ondelete='CASCADE'),
                            primary_key=True),
                     Column('tag_id', String(60),
                            ForeignKey('tags.id', onupdate='CASCADE',
                                       ondelete='CASCADE'),
                            primary_key=True))


class Project(BaseModel, Base):
    """This class defines a user by attributes"""
    __tablename__ = 'projects'
    name = Column(String(128))
    description = Column(Text(2000))
    background_image = Column(
        String(20),
        nullable=False,
        default="default.jpg")
    github_link = Column(String(128), nullable=False)
    demo_link = Column(String(128))
    tags = Column(JSON)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
