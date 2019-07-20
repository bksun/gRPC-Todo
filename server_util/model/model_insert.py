from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from model import Todo, Base, User
from DAL import dal

dal.connect()
session = dal.Session()
# Insert a User in the User table
new_user = User(name='sksun')
session.add(new_user)
session.commit()
 
# Insert an Todo in the Todo table
new_todo = Todo(text='Another todo by sksun from sql-alchemy', isdone=False, user=user)
session.add(new_todo)
session.commit()