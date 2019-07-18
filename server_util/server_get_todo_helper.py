from concurrent import futures
import time
import math
import logging
import grpc
import todo_pb2
import todo_pb2_grpc
import todo_resources

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

def get_todo(todo_db, request):
    """Returns todo at given location or None."""
    for todo in todo_db:
        if todo.id == request.id:
            todo.status = todo_pb2.SUCCESS
            return todo
    request.status = todo_pb2.FAILED
    return request

class RouteGuideServicer(todo_pb2_grpc.RouteGuideServicer):
    def __init__(self):
        self.db = todo_resources.read_todo_database()
        # print(self.db)

    def GetTodo(self, request, context):
        todo = get_todo(self.db, request)
        if todo is None:
            return todo_pb2.Todo(id=request.id)
        else:
            return todo

    def AddTodo(self, todo, context):
        if isinstance(todo, todo_pb2.Todo):
            todo.id = len(self.db)+1
            # import ipdb; ipdb.set_trace()
            self.db.append(todo)
            todo.status = todo_pb2.SUCCESS
            return todo
        else:
            todo.status = todo_pb2.FAILED
            return todo

    def RemoveTodoHelper(self, request):
        for todo in self.db:
            if todo.id == request.id:
                a = self.db.remove(todo)
                print(a)

    def RemoveTodo(self, request, context):
        self.RemoveTodoHelper(request)
        print('Server - Addtodo - req:', request)
        request.status = todo_pb2.SUCCESS
        return request

    def ListTodoByUser(self, request, context):
        if isinstance(request, todo_pb2.User):
            for todo in self.db:
                if todo.user.name ==  request.name:
                    todo.status = todo_pb2.SUCCESS
                    yield todo
                else:
                    pass

    def ListTodoByStatus(self, request, context):
        for todo in self.db:
            if todo.isdone == False:
                yield todo
            else:
                print(todo.isdone)
