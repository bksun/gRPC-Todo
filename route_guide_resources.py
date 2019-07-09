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
            todo = todo_pb2.todo(
                name=item["name"],
                location=todo_pb2.Point(
                    latitude=item["location"]["latitude"],
                    longitude=item["location"]["longitude"]))
            todo_list.append(todo)
    print(todo_list[0])

    return todo_list
