import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class User(Base):
    __tablename__ = 'user'
    # Here we define columns for the table user
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
 
class Todo(Base):
    __tablename__ = 'todo'
    # Here we define columns for the table todo.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    text = Column(String(250))
    isdone = Column(Boolean)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
# engine = create_engine('sqlite:///TodoApp-DB.db')
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
# Base.metadata.create_all(engine)
