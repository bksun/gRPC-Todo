from __future__ import print_function
import random
import logging
import grpc
import todo_pb2
import todo_pb2_grpc
import todo_resources
from client_helper.client_get_todo_helper import *


def input_helper():
		print('1. To view a todo')
		print('2. To view all todo')
		print('3. To add new todo')
		print('4. To remove a todo')

def run():
	# NOTE(gRPC Python Team): .close() is possible on a channel and should be
	# used in circumstances in which the with statement does not fit the needs
	# of the code.

	input_helper()

	with grpc.insecure_channel('localhost:50051') as channel:
		stub = todo_pb2_grpc.RouteGuideStub(channel)
		while True:
			try:
				user_input = int(input('Please enter your input:'))
				if user_input == 1:
					input_action = int(input('Please enter a ID to view:'))
					print("-------------- Gettodo --------------")
					guide_get_todo(stub, input_action)
				elif user_input == 2:
					print("-------------- Listtodos --------------")
					guide_list_todos(stub)
				elif user_input == 3:
					input_action = str(input('Please enter a message to add:'))
					print("-------------- Add todo --------------")
					Add_one_todo(stub, input_action)
				elif user_input == 4:
					input_action = int(input('Please enter a ID to delete:'))
					print("-------------- Gettodo --------------")
					remove_one_todo(stub, input_action)
			except ValueError as ve:
				print('Please enter integer value only.')
		# print("-------------- Gettodo --------------")
		# guide_get_todo(stub)
		# print("-------------- Listtodos --------------")
		# guide_list_todos(stub)
		# print("-------------- Add todos --------------")
		# Add_one_todo(stub)
		# print("-------------- Gettodo --------------")
		# remove_one_todo(stub)
		

if __name__ == '__main__':
	logging.basicConfig()
	run()