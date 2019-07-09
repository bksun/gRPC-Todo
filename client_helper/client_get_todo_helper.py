from __future__ import print_function
import random
import logging
import grpc
import todo_pb2
import todo_pb2_grpc
import todo_resources
# def make_route_note(message, latitude, longitude):
#     return todo_pb2.RouteNote(
#         message=message,
#         location=todo_pb2.Point(latitude=latitude, longitude=longitude))


def guide_get_one_todo(stub, point):
    print('Client - Ready for GetTodo called..')
    todo = stub.GetTodo(point)
    print('Client - GetTodo called..')
    if not todo.id:
        print("Server returned incomplete todo")
        return

    if todo.msg:
        print("todo called %s at %s" % (todo.id, todo.msg))
    else:
        print("Found no todo at %s" % todo.id)


def guide_get_todo(stub):
    guide_get_one_todo(stub, todo_pb2.TodoCode(id=10))
    guide_get_one_todo(stub, todo_pb2.TodoCode(id=0))
