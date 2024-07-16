#./api/models/colony.py
'''module for defining the `colony` models that will be used to perform CRUD operations on the database and
The models that will be used as schemas/response/request data in the API schema. All SQLModels'''
from sqlmodel import SQLModel, Field
from app.models.players import PlayerInfo

class BaseColony(SQLModel):
    'base class for a colony'
    number: int
    players: list[PlayerInfo]