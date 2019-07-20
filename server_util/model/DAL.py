from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class DataAccessLayer:
    def __init__(self, db_path='todo.sqlite3'):
        self.engine = None
        self.Session = None
        self.conn_string = 'sqlite:///TodoApp-DB.db?check_same_thread=False'

    def connect(self):
        self.engine = create_engine(self.conn_string)
        Base.metadata.bind = self.engine
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)


dal = DataAccessLayer()