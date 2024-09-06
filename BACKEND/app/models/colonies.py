#./api/models/colony.py
'''module for defining the `colony` models that will be used to perform CRUD operations on the database and
The models that will be used as schemas/response/request data in the API schema. All SQLModels'''
from sqlmodel import Field, Relationship
from app.models.bases import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.players import Player
    from .matches import Match


# write your colony models here

class Colony(BaseColony, table=True):
    id: int | None = Field(default=None, primary_key=True)
    players: list["Player"] | None = Relationship(back_populates="colony")
    matches: list["Match"] | None = Relationship(back_populates="colony")

# CLIENT SIDE RESPONSE MODELS
class ColonyInfo(BaseColonyInfo):
    'colony info -> client-side'
    players: list[BasePlayerInfo]