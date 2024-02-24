#!/user/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, ForeignKey


class Comment(BaseModel, Base):
    """This class defines a user by attributes"""

    __tablename__ = "comments"
    body = Column(String(512), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    project_id = Column(String(60), ForeignKey("projects.id"), nullable=False)