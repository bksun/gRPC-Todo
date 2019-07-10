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

		def guide_list_todos(self):
			print('List Todo called..')
			list_todos = todo_pb2.Mode(id = 1)
			print("inside guide_list" , list_todos)
			todos = self.stub.ListTodos(list_todos)
			for todo in todos:
				print("todo called %s at %s" % (todo.id, todo.msg))


		def Add_one_todo(self, input_action):
			print('Client - Ready Post Call..')

			todos = self.stub.AddTodo(todo_pb2.Todo(
				msg=input_action
			))

			print('Client - Post call over..')
			for todo in todos:
				print("todo: ", todo)

		def remove_one_todo(self, input_action):
			todos = self.stub.RemoveTodo(todo_pb2.TodoCode(id=input_action))
			print('Printing todos after removal...')
			for todo in todos:
				print("todo: ", todo)

		def guide_get_one_todo(self, point):
			print('Client - Ready for GetTodo called..')
			todo = self.stub.GetTodo(point)
			print('Client - GetTodo called..')
			if not todo.id:
				print("Server returned incomplete todo")
				return

			if todo.msg:
				print("todo called %s at %s" % (todo.id, todo.msg))
			else:
				print("Found no todo at %s" % todo.id)

		def guide_get_todo(self, user_input):
			self.guide_get_one_todo(todo_pb2.TodoCode(id=user_input))

