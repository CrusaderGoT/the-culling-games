'''a module that handles the connection of sqlmodel to postgresql'''
from sqlmodel import SQLModel, create_engine


# create the engine
def sql_engine():
    '''This returns the engine object from sqlmodel create_engine().
    \nSide-Effect: Creates all models table(sqlmodel's with table = True),
    using SQLModel.metadata.create_all(engine).
    \nAccording to the sqlmodel docs:
    You should normally have a single engine object for your whole
    application and re-use it everywhere.
    \n Example:
    \n## import sql_engine after all models (sqlmodel) are imported.
    \n>>> from models.py import all_models # example of importing all models
    \n>>> from pgsql import sql_engine
    \n>>> engine = sql_engine()
    '''
    # the database url
    DATABASE_URL = "postgresql://postgres:crusader@localhost/CullingGamesDB"
    # this makes sure ?
    #connect_args = {"check_same_thread": False}
    #Create the engine using the URL.
    engine = create_engine(DATABASE_URL, echo=True) # echo makes it print the sql statement.
    #Create all the tables that were automatically registered in SQLModel.metadata.
    SQLModel.metadata.create_all(engine)
    return engine