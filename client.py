from __future__ import print_function
import random
import logging
import grpc
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
				print("-------------- Gettodo --------------")
				client_stub.guide_get_todo(input_action)
			elif user_input == 2:
				print("-------------- Listtodos --------------")
				client_stub.guide_list_todos()
			elif user_input == 3:
				input_action = str(input('Please enter a message to add:'))
				print("-------------- Add todo --------------")
				client_stub.Add_one_todo(input_action)
			elif user_input == 4:
				input_action = int(input('Please enter a ID to delete:'))
				print("-------------- Gettodo --------------")
				client_stub.remove_one_todo(input_action)
		except ValueError as ve:
			print(ve)
			print('Please enter integer value only.')		


if __name__ == '__main__':
	logging.basicConfig()
	run()