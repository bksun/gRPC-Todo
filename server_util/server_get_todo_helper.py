from concurrent import futures
import time
import math
import logging
import grpc
import todo_pb2
import todo_pb2_grpc
import todo_resources
from sqlalchemy.orm import exc

from server_util.model.DAL import dal
from server_util.model.model import Todo, User


class RouteGuideServicer(todo_pb2_grpc.RouteGuideServicer):
    def __init__(self, db_session=None):
        self.db = todo_resources.read_todo_database()
        if db_session:
            self.session = db_session
        else:
            dal.connect()
            self.session = dal.Session()
    
    def get_todo(self, request):
        """Returns todo at given location or None."""
        todo = self.session.query(Todo).filter(Todo.id==request.id).one()
        if todo.id == request.id:
            return todo
        return request

    def GetTodo(self, request, context):
        todo = self.get_todo(request)
        if todo is None:
            return todo_pb2.Todo(id=request.id, status=todo_pb2.FAILED)
        else:
            todo.status = todo_pb2.SUCCESS
            todo = self.ConvertTodoModelTogRPC(todo)
            todo.status = todo_pb2.SUCCESS
            return todo

    def AddTodo(self, todo, context):
        if isinstance(todo, todo_pb2.Todo):
            import ipdb; ipdb.set_trace()
            user = self.session.query(User).filter(User.name==todo.user.name).one()
            
            if isinstance(user, User):
                    new_todo = Todo(
                    text=todo.text,
                    isdone=todo.isdone,
                    user=user
                    )
                    # print(new_todo.text, new_todo.isdone, new_todo.user.name)
                    self.session.add(new_todo)
                    self.session.commit()
            elif user is None:
                user = User(name="sksun")
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
        except exe.NoResultFound:
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
            user = self.session.query(User).filter(User.name==request.name).one()
            # for user in users:
            #     self.session.delete(user)
            #     self.session.commit()
            todos = self.session.query(Todo).filter(Todo.user==user).all()
            # for user in todos:
            #     self.session.delete(user)
            #     self.session.commit()
            for todo in todos:
                todo =  self.ConvertTodoModelTogRPC(todo)
                yield todo

    def ListTodoByStatus(self, request, context):
        import ipdb; ipdb.set_trace()
        todos = self.session.query(Todo).filter(Todo.isdone==False)
        for todo in todos:
            todo = self.ConvertTodoModelTogRPC(todo)
            yield todo
