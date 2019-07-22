from concurrent import futures
import time
import math
import logging
import grpc
import todo_pb2
import todo_pb2_grpc
import todo_resources
from server_util.server_helper import *

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


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
