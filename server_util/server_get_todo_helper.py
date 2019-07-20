from concurrent import futures
import time
import math
import logging
import grpc
import todo_pb2
import todo_pb2_grpc
import todo_resources

from server_util.model.DAL import dal
from server_util.model.model import Todo, User


def get_todo(todo_db, request):
    """Returns todo at given location or None."""
    for todo in todo_db:
        if todo.id == request.id:
            todo.status = todo_pb2.SUCCESS
            return todo
    request.status = todo_pb2.FAILED
    return request

class RouteGuideServicer(todo_pb2_grpc.RouteGuideServicer):
    def __init__(self, db_session=None):
        self.db = todo_resources.read_todo_database()
        if db_session:
            self.session = db_session
        else:
            dal.connect()
            self.session = dal.Session()


    def GetTodo(self, request, context):
        todo = get_todo(self.db, request)
        if todo is None:
            return todo_pb2.Todo(id=request.id)
        else:
            return todo

    def AddTodo(self, todo, context):
        if isinstance(todo, todo_pb2.Todo):
            # import ipdb; ipdb.set_trace()
            user = self.session.query(User).filter(User.name==todo.user.name).first()
            if user is None:
                user = User(name="bksun")
            if isinstance(user, User):
                    new_todo = Todo(
                    text=todo.text,
                    isdone=todo.isdone,
                    user=user
                    )
                    # print(new_todo.text, new_todo.isdone, new_todo.user.name)
                    self.session.add(new_todo)
                    self.session.commit()
            todo.status = todo_pb2.SUCCESS
            return todo
        else:
            todo.status = todo_pb2.FAILED
            return todo

    def ConvertTodoModelTogRPC(self, todo):
        todo = todo_pb2.Todo(
                    text=todo.text,
                    id=todo.id,
                    user= todo_pb2.User(name=todo.user.name),
                    isdone=todo.isdone,
                    status=todo.status
                )
        return todo

    def RemoveTodoHelper(self, request):
        todo = self.session.query(Todo).filter(id==request.id).\
        delete(synchronize_session='evaluate')
        import ipdb; ipdb.set_trace()
        print(todo)
        todo = self.ConvertTodoModelTogRPC(todo=todo_pb2.Todo(status=todo_pb2.FAILED))
        return todo

    def RemoveTodo(self, request, context):
        self.RemoveTodoHelper(request)
        print('Server - Remove-todo - req:', request)
        request.status = todo_pb2.SUCCESS
        return request

    def ListTodoByUser(self, request, context):
        if isinstance(request, todo_pb2.User):
            todos = self.session.query(Todo).all()
            for todo in todos:
                todo =  self.ConvertTodoModelTogRPC(todo)
                yield todo

    def ListTodoByStatus(self, request, context):
        todos = self.session.query(Todo).filter(Todo.isdone==False)
        for todo in todos:
            todo = self.ConvertTodoModelTogRPC(todo)
            yield todo
