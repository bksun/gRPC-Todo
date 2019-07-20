from __future__ import print_function
import random
import logging
import grpc
import todo_pb2
import todo_pb2_grpc
import todo_resources


class ClientStub:
		def __init__(self):
			channel = grpc.insecure_channel('localhost:50051')
			stub = todo_pb2_grpc.RouteGuideStub(channel)
			self.stub = stub
			print('Client stub initialized..')

		def list_todos_by_status(self):
			list_todos = todo_pb2.Todo(isdone = True)
			todos = self.stub.ListTodoByStatus(list_todos)
			for todo in todos:
				print("todo added with %s, %s, %s" % (todo.id, todo.text, todo.user.name))

		def list_todos_by_user(self, username):
			list_todos = todo_pb2.User(name=username)
			todos = self.stub.ListTodoByUser(list_todos)
			for todo in todos:
				print("todo added with %s, %s, %s" % (todo.id, todo.text, todo.user.name))

		def add_one_todo(self, input_action):
			todo = self.stub.AddTodo(
				todo_pb2.Todo(
				text=input_action,
				user=todo_pb2.User(name="sksun"),
				isdone=False
			))
			if todo.status == todo_pb2.FAILED:
				print("FAILED: todo not added!", todo)
			else:
				print("todo added with %s and %s" % (todo.id, todo.text))

		def remove_one_todo(self, input_action):
			todo = self.stub.RemoveTodo(todo_pb2.Todo(id=input_action))
			if todo.status == todo_pb2.SUCCESS:
				print("todo with id: %s removed" % (todo.id))
			else:
				print("todo not removed")

		def get_one_todo_util(self, point):
			todo = self.stub.GetTodo(point)
			if todo.status == todo_pb2.FAILED:
				print("Server returned incomplete todo")
			else:
				print("todo called %s at %s" % (todo.id, todo.text))

		def get_todo(self, user_input):
			self.get_one_todo_util(todo_pb2.Todo(id=user_input))

