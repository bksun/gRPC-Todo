from concurrent import futures
import time
import math
import logging
import grpc
import todo_pb2
import todo_pb2_grpc
import todo_resources

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

def get_todo(todo_db, point):
    """Returns todo at given location or None."""
    for todo in todo_db:
        if todo.id == point:
            return todo
    return None


class RouteGuideServicer(todo_pb2_grpc.RouteGuideServicer):
    def __init__(self):
        self.db = todo_resources.read_todo_database()
        # print(self.db)

    def GetTodo(self, request, context):
        print('Server - Get Todo called..')
        todo = get_todo(self.db, request)
        print('server - request:', request)
        if todo is None:
            return todo_pb2.Todo(msg="", id=request)
        else:
            return todo

    def AddTodo(self, request, context):
        print('Server - Get Todo called..')
        # todo = get_todo(self.db, request)
        new_request = todo_pb2.Todo(
                        id=todo_pb2.TodoCode(id=len(self.db)+1),
                        msg=request.msg
                        )
        self.db.append(new_request)
        print('Server - Addtodo - req:', new_request.id)
        for todo in self.db:
            yield todo

    # def StreamTodos(self, request, context):
    #     print("inside stream todo")
    #     for todo in self.db:
    #             yield todo

    def RemoveTodoHelper(self, request):
        for todo in self.db:
            if todo.id == request:
                self.db.remove(todo)

    def RemoveTodo(self, request, context):
        print('Server - Get Todo called..')
        self.RemoveTodoHelper(request)

        print('Server - Addtodo - req:', request)
        for todo in self.db:
                yield todo

    def ListTodos(self, request, context):
        print(request)
        # self.StreamTodos(request, context)
        for todo in self.db:
               yield todo        
