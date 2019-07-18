from __future__ import print_function
import random
import logging
# import grpc
import todo_pb2
import todo_pb2_grpc
import todo_resources
from client_util.client_get_todo_helper import *

def input_helper():
		print('1. To view a todo')
		print('2. To view all todo')
		print('3. To add new todo')
		print('4. To remove a todo')

def run():

	input_helper()

	client_stub = ClientStub()
	while True:
		try:
			user_input = int(input('Please enter your input:'))
			if user_input == 1:
				input_action = int(input('Please enter a ID to view:'))
				client_stub.get_todo(input_action)
			elif user_input == 2:
				input_action = int(input('By User: 1, By Status: 2:'))
				if input_action == 1:
					username = input('Please enter username:')
					client_stub.list_todos_by_user(username)
				else:
					client_stub.list_todos_by_status()
			elif user_input == 3:
				input_action = str(input('Please enter a message to add:'))
				client_stub.add_one_todo(input_action)
			elif user_input == 4:
				input_action = int(input('Please enter a ID to delete:'))
				client_stub.remove_one_todo(input_action)
			elif user_input > 4:
				raise ValueError
		except ValueError as ve:
			print(ve)
			print('Please enter value from 1 to 4 only.')		


if __name__ == '__main__':
	logging.basicConfig()
	run()