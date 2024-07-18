#./api/models/colony.py
'''module for defining the `colony` models that will be used to perform CRUD operations on the database and
The models that will be used as schemas/response/request data in the API schema. All SQLModels'''
from sqlmodel import SQLModel, Field, Relationship
from pydantic import FilePath, FileUrl
from typing import Union
from app.models.players import Player, PlayerInfo
from app.models.bases import *
from enum import Enum
from datetime import datetime


# write your colony and match models here

class Enviroment(Enum):
    ice = "ice"
    fire = "fire"
    air = "air"

# COLONY


class Colony(BaseColony, table=True):
    id: int | None = Field(default=None, primary_key=True)
    players: list[Player] | None = Relationship(back_populates="colony")
    #matches: list["Match"] | None = Relationship(back_populates="colony")
    
class ColonyInfo(BaseColonyInfo):
    'colony info -> client-side'
    players: list[BasePlayerInfo]
    #matches: list["BaseMatchInfo"] | None = None

"""# MATCH
class MatchPlayerLink(SQLModel, table=True):
    match_id: int | None = Field(default=None, primary_key=True)
    player_id: int | None = Field(default=None, primary_key=True)

class BaseMatch(SQLModel):
    begin: datetime
    end: datetime

class Match(BaseMatch, table=True):
    id: int | None = Field(default=None, primary_key=True)
    colony_id: int = Field(foreign_key='colony.id')
    colony: Colony = Relationship(back_populates="matches")
    location_id: int = Field(foreign_key='location.id')
    location: "Location" = Relationship(back_populates="matches")
    players: list[Player] = Relationship(back_populates="matches",
                                         link_model="MatchPlayerLink")
    winner_id: int = Field(foreign_key='player.id', description="The winner of the match ID (player Id)")
    winner: Union["Player", None] = Relationship(back_populates="matches_won")
    
class BaseMatchInfo(BaseMatch):
    id: int
    winner: BasePlayerInfo

class MatchInfo(BaseMatchInfo):
    players: list[BasePlayerInfo]


class Location(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    latitude: float | None = Field(default=None)
    longitude: float | None = Field(default=None)
    image: FilePath | FileUrl
    enviromental_condition: "Enviroment"
    matches: list["Match"] = Relationship(back_populates="location")
"""