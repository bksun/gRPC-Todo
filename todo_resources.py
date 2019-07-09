import json

import todo_pb2


def read_todo_database():
    """Reads the route guide database.
  Returns:
    The full contents of the route guide database as a sequence of
      todo_pb2.todos.
  """
    todo_list = []
    with open("todo_db.json") as todo_db_file:
        for item in json.load(todo_db_file):
            todo = todo_pb2.Todo(
                msg=item["msg"],
                id=todo_pb2.TodoCode(id=item["id"]))
            todo_list.append(todo)
    # print(todo_list[0])

    return todo_list