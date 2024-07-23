#./api/models/match.py
'''module for defining the `match` `location` and `vote` models that will be used to perform CRUD operation
on the database and will be used as schemas/response/request data in the API schema. All SQLModels'''
from sqlmodel import SQLModel, Field, Relationship
from pydantic import FileUrl, FilePath
from datetime import datetime
from app.models.bases import *
from typing import TYPE_CHECKING, Union
if TYPE_CHECKING:
    from app.models.players import Player
    from app.models.colony import Colony

# MATCH
class BaseMatch(SQLModel):
    begin: datetime
    end: datetime


class Match(BaseMatch, table=True):
    id: int | None = Field(default=None, primary_key=True)
    location_id: int = Field(foreign_key='location.id')
    location: "Location" = Relationship(back_populates="matches")

    #players: list["Player"] = Relationship(back_populates="matches", link_model=MatchPlayerLink)
    
    #winner_id: int = Field(foreign_key='player.id', description="The winner of the match ID (player Id)")
    #winner: Union["Player", None] = Relationship(back_populates="wins")

class BaseLocation(SQLModel):
    latitude: float | None = Field(default=None)
    longitude: float | None = Field(default=None)
    image: FilePath | FileUrl
    enviromental_condition: str

class Location(BaseLocation, table=True):
    id: int | None = Field(default=None, primary_key=True)
    colony_id: int = Field(foreign_key='colony.id')
    colony: "Colony" = Relationship(back_populates="locations")
    matches: list["Match"] = Relationship(back_populates="location")


class BaseMatchInfo(BaseMatch):
    id: int
    winner: BasePlayerInfo

class MatchInfo(BaseMatchInfo):
    players: list[BasePlayerInfo]



