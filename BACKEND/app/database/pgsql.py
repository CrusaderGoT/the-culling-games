'''a module that handles the connection of sqlmodel to postgresql\n
The engine object can be import from this module'''
from sqlmodel import SQLModel, create_engine
from os import environ


DATABASE_URL = environ["DATABASE_URL"]
# create engine variable
engine = create_engine(DATABASE_URL, echo=True)

def create_db_tables():
    "Create all the tables that were automatically registered in SQLModel.metadata."
    SQLModel.metadata.create_all(engine)