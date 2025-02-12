#./api/models/colony.py
'''module for defining the `colony` models that will be used to perform CRUD operations on the database and
The models that will be used as schemas/response/request data in the API schema. All SQLModels'''
from sqlmodel import Field, Relationship
from ..models.base import BaseColony, BaseColonyInfo, BasePlayerInfo
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.player import Player
    from .match import Match


# write your colony models here

# COLONY
class Colony(BaseColony, table=True):
    'a colony as stored in the database'
    id: int | None = Field(default=None, primary_key=True)
    players: list["Player"] = Relationship(back_populates="colony")
    matches: list["Match"] = Relationship(back_populates="colony")

# CLIENT SIDE RESPONSE MODELS
class ColonyInfo(BaseColonyInfo):
    'colony info -> client-side'
    players: list[BasePlayerInfo]
