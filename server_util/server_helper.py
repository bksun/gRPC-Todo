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
from server_util.server_util_functions import utils
from server_util.model.model import Todo, User

DEFAULT_USER = "sksun"

class RouteGuideServicer(todo_pb2_grpc.RouteGuideServicer):
    def __init__(self, db_session=None):
        self.db = todo_resources.read_todo_database()
        if db_session:
            self.session = db_session
        else:
            dal.connect()
            self.session = dal.Session()
    
    def GetTodo(self, request, context):
        todo = utils.get_one_todo(request)
        if todo.status != todo_pb2.SUCCESS:
            return todo_pb2.Todo(id=request.id, status=todo_pb2.FAILED)
        else:
            todo = self.ConvertTodoModelTogRPC(todo)
            todo.status = todo_pb2.SUCCESS
            return todo

    def AddTodo(self, todo, context):
        if isinstance(todo, todo_pb2.Todo):
            import ipdb; ipdb.set_trace()
            try:
                user = self.session.query(User).filter(User.name==todo.user.name).one()
            except exc.NoResultFound:
                user = User(name=todo.user.name)
            finally:
                if isinstance(user, User):
                        new_todo = Todo(
                        text=todo.text,
                        isdone=todo.isdone,
                        user=user
                        )
                        self.session.add(new_todo)
                        self.session.commit()
                        todo.status = todo_pb2.SUCCESS
                        return todo
                elif user is None:
                    user = User(name=DEFAULT_USER)
                return todo
        else:
            todo.status = todo_pb2.FAILED
            return todo

    def ConvertTodoModelTogRPC(self, todo):
        todo = todo_pb2.Todo(
                    text=todo.text,
                    id=todo.id,
                    user= todo_pb2.User(name=todo.user.name),
                    isdone=todo.isdone
                )
        return todo

    def RemoveTodoHelper(self, request):
        try:
            import ipdb; ipdb.set_trace()
            todo = self.session.query(Todo).filter(Todo.id==request.id).one()
            self.session.delete(todo)
            self.session.commit()
            todo.status = todo_pb2.SUCCESS
            return todo
        except exc.NoResultFound:
            return todo_pb2.Todo(status=todo_pb2.FAILED)

    def RemoveTodo(self, request, context):
        import ipdb; ipdb.set_trace()
        todo = self.RemoveTodoHelper(request)
        if todo.status == todo_pb2.FAILED:
            return request
        todo = self.ConvertTodoModelTogRPC(todo)
        return todo

    def ListTodoByUser(self, request, context):
        import ipdb; ipdb.set_trace()
        if isinstance(request, todo_pb2.User):
            try:
                username = request.name
                todos = utils.list_by_user(username)
                for todo in todos:
                    todo =  self.ConvertTodoModelTogRPC(todo)
                    todo.status = todo_pb2.SUCCESS
                    yield todo
            except exc.NoResultFound:
                todo = todo_pb2.Todo(status=todo_pb2.FAILED)
                yield todo

    def ListTodoByStatus(self, request, context):
        import ipdb; ipdb.set_trace()
        # status = request.isdone
        status = True
        todos = utils.list_by_status(status)
        for todo in todos:
            todo = self.ConvertTodoModelTogRPC(todo)
            yield todo
