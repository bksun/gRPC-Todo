from __future__ import print_function
import random
import logging
import grpc
import todo_pb2
import todo_pb2_grpc
import todo_resources
from client_helper.client_get_todo_helper import *


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = todo_pb2_grpc.RouteGuideStub(channel)
        print("-------------- Gettodo --------------")
        guide_get_todo(stub)
        # print("-------------- Listtodos --------------")
        # guide_list_todos(stub)
        # print("-------------- RecordRoute --------------")
        # guide_record_route(stub)
        # print("-------------- RouteChat --------------")
        # guide_route_chat(stub)


if __name__ == '__main__':
    logging.basicConfig()
    run()