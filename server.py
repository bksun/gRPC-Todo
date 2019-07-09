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
        if todo is None:
            return todo_pb2.Todo(msg="", id=request)
        else:
            return todo


def serve():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        todo_pb2_grpc.add_RouteGuideServicer_to_server(
        RouteGuideServicer(), server)
        server.add_insecure_port('[::]:50051')
        server.start()
        try:
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()
    serve()
