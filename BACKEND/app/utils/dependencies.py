'''module for defining fastapi dependencies'''
from app.database.pgsql import engine
from sqlmodel import Session

# Get Session Dependency
def get_session():
    'yields a session'
    with Session(engine) as session:
        print(id(engine), 'first engineeeeeeeeeeeeeeeeeeeeee')
        yield session