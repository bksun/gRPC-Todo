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

    def ListTodos(self, request, context):

        for feature in self.db:
            # if (feature.location.longitude >= left and
            #         feature.location.longitude <= right and
            #         feature.location.latitude >= bottom and
            #         feature.location.latitude <= top):
                yield feature
