from __future__ import print_function
import random
import logging
import grpc
import todo_pb2
import todo_pb2_grpc
import todo_resources

from client_util.client_util_functions import *


class ClientStub:
		def __init__(self):
			channel = grpc.insecure_channel('localhost:50051')
			stub = todo_pb2_grpc.RouteGuideStub(channel)
			self.stub = stub
			print('Client stub initialized..')

		def list_todos_by_status(self, status):
			if status == 1:
				list_todos = todo_pb2.Todo(isdone = True)
			else:
				list_todos = todo_pb2.Todo(isdone = False)

			todos = self.stub.ListTodoByStatus(list_todos)
			count = count_iterable(todos)
			if count > 0:
				print(count)
				for todo in todos:
					print("todo added with %s, %s, %s" % (todo.id, todo.text, todo.user.name))
			else:
				print("No list with given status")
	
		def list_todos_by_user(self, username):
			username = todo_pb2.User(name=username)
			todos = self.stub.ListTodoByUser(username)
			for todo in todos:
				if todo.status == todo_pb2.SUCCESS:
					print("todo with %s, %s, %s" % (todo.id, todo.text, todo.user.name))
				else:
					print("todo not found with username: %s" %(username))

		def add_one_todo(self, input_action, username):
			todo = self.stub.AddTodo(
				todo_pb2.Todo(
				text=input_action,
				user=todo_pb2.User(name=username),
				isdone=False,
				status=todo_pb2.SUCCESS
			))
			if todo.status == todo_pb2.FAILED:
				print("FAILED: todo not added!", todo)
			else:
				print("todo added with %s " % (todo.text))

		def remove_one_todo(self, input_action):
			todo = self.stub.RemoveTodo(todo_pb2.Todo(id=input_action))
			if todo.status == todo_pb2.SUCCESS:
				print("todo with id: %s removed" % (input_action))
			else:
				print("todo not removed")

		def get_one_todo_util(self, point):
			todo = self.stub.GetTodo(point)
			if todo.status == todo_pb2.FAILED:
				print("Server has no todo with ID: %s " % (point.id))
			else:
				print("todo called ID: %s with todo: %s" % (todo.id, todo.text))

		def get_todo(self, user_input):
			self.get_one_todo_util(todo_pb2.Todo(id=user_input))
