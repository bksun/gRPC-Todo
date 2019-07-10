from __future__ import print_function
import random
import logging
import grpc
import todo_pb2
import todo_pb2_grpc
import todo_resources

def guide_list_todos(stub):
    list_todos = todo_pb2.Mode(id = 1)
    todos = stub.ListTodos(list_todos)
    for todo in todos:
        print("todo called %s at %s" % (todo.id, todo.msg))


def Add_one_todo(stub, input_action):
    print('Client - Ready Post Call..')
    # one_todo = todo_pb2.Todo()
    # one_todo.id = 200
    # one_todo.msg = "My message"

    todos = stub.AddTodo(todo_pb2.Todo(
        msg=input_action
    ))

    print('Client - Post call over..')
    for todo in todos:
        print("todo: ", todo)

def remove_one_todo(stub, input_action):
    todos = stub.RemoveTodo(todo_pb2.TodoCode(id=input_action))
    print('Printing todos after removal...')
    for todo in todos:
        print("todo: ", todo)

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


def guide_get_todo(stub, user_input):
    guide_get_one_todo(stub, todo_pb2.TodoCode(id=user_input))
    # guide_get_one_todo(stub, todo_pb2.TodoCode(id=0))
