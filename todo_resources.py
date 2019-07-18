import json

import todo_pb2


def read_todo_database():
    """Reads the to-do database.
  Returns:
    The full contents of the to-do database as a sequence of
      todo_pb2.todos.
  """
    todo_list = []

    with open("todo_db.json") as todo_db_file:
        for item in json.load(todo_db_file):
            todo = todo_pb2.Todo(
                id=item["id"],
                text=item["text"],
                user=todo_pb2.User(name=item["user"]),
                isdone=item["isdone"],
                )
            todo_list.append(todo)
           
    return todo_list
