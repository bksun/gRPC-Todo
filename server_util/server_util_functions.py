from concurrent import futures
import time
import math
import logging
import grpc
import todo_pb2
import todo_pb2_grpc
import todo_resources
from sqlalchemy.orm import exc

from server_util.model.dal import dal
from server_util.model.model import Todo, User

DEFAULT_USER = "sksun"

class ServerUtils:
    def __init__(self, db_session=None):
        self.db = todo_resources.read_todo_database()
        if db_session:
            self.session = db_session
        else:
            dal.connect()
            self.session = dal.Session()

    def status_success(self):
        return todo_pb2.SUCCESS

    def status_failed(self):
        return todo_pb2.FAILED

    def get_one_todo(self, request):
        """Returns todo at given location or None."""
        try:
            todo = self.session.query(Todo).filter(Todo.id==request.id).one()
            if todo.id == request.id:
                todo.status = self.status_success()
                return todo
        except exc.NoResultFound:
            request.status = self.status_failed()
            return request

    def get_user(self, username):
        """Returns user object"""
        try:
            user = self.session.query(User).filter(User.name==username).one()
            if isinstance(user, User):
                return user
        except exc.NoResultFound:
            raise exc.NoResultFound

    def get_unread_status(self):
        """Returns False status (for unread todo)"""
        return False
  
    def get_read_status(self):
        """Returns True status (for read todo)"""
        return True

    def list_by_user(self, username):
        try:
            user = self.get_user(username)
            todos = self.session.query(Todo).filter(Todo.user==user).all()
            return todos
        except exc.NoResultFound:
            raise exc.NoResultFound

    def list_by_status(self, status):
        try:
            if status:
                todos = self.session.query(Todo).filter(Todo.isdone==self.get_unread_status()).all()
                return todos
            else:
                todos = self.session.query(Todo).filter(Todo.isdone==self.get_read_status()).all()
                return todos
 
        except exc.NoResultFound:
            raise exc.NoResultFound

utils = ServerUtils()
