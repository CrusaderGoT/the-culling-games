#./api/models/match.py
'''module for defining the `match` `location` and `vote` models that will be used to perform CRUD operation
on the database and will be used as schemas/response/request data in the API schema. All SQLModels'''
from sqlmodel import SQLModel, Field, Relationship
from pydantic import FileUrl, FilePath
from datetime import datetime
from app.models.bases import MatchPlayerLink, BaseColonyInfo, BasePlayerInfo
from typing import TYPE_CHECKING, Union
if TYPE_CHECKING:
    from app.models.players import Player 
    from app.models.colonies import Colony

# MATCH
class BaseMatch(SQLModel):
    """Base match model
    \nbegin: datetime
    \nend: datetime"""
    begin: datetime
    end: datetime
    part: int

class Match(BaseMatch, table=True):
    'a match as stored in the database'
    id: int | None = Field(default=None, primary_key=True)

    colony_id: int = Field(foreign_key='colony.id')
    colony: "Colony" = Relationship(back_populates="matches")

    #typically will have only two unique players in a match
    players: list["Player"] = Relationship(back_populates="matches", link_model=MatchPlayerLink)

class BaseMatchInfo(BaseMatch):
    'base match info, without player, colony infos.'
    id: int

class MatchInfo(BaseMatchInfo):
    'match info for client side'
    players: list["BasePlayerInfo"]
    colony: "BaseColonyInfo"


""" 

    location_id: int = Field(foreign_key='location.id')
    location: "Location" = Relationship(back_populates="matches")
    
    
    #winner_id: int | None = Field(foreign_key='player.id', description="The winner of the match ID (player Id)")
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
    # typically a location will have just one match
    # the m_2_1 relation is a fallback for situations a location has to be used again
    matches: list["Match"] = Relationship(back_populates="location")



"""