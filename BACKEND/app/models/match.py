#./api/models/match.py
'''module for defining the `match` `location` and `vote` models that will be used to perform CRUD operation
on the database and will be used as schemas/response/request data in the API schema. All SQLModels'''
from sqlmodel import Field, Relationship, SQLModel
from app.models.base import (BaseMatch, BaseMatchInfo, MatchPlayerLink,
                             BaseColonyInfo, BasePlayerInfo, BaseUserInfo,
                             BaseCTAppInfo)
from typing import TYPE_CHECKING, Union
from datetime import time
if TYPE_CHECKING:
    from app.models.player import Player, CTApp
    from app.models.colony import Colony
    from .user import User

# MATCH
class Match(BaseMatch, table=True):
    'a match as stored in the database'
    id: int | None = Field(default=None, primary_key=True)
    colony_id: int | None = Field(foreign_key='colony.id')
    colony: "Colony" = Relationship(back_populates="matches")
    #typically will have only two unique players in a match
    players: list["Player"] = Relationship(back_populates="matches", link_model=MatchPlayerLink)
    winner_id: int | None = Field(default=None, foreign_key='player.id', description="The winner of the match ID (player Id)")
    winner: Union["Player", None] = Relationship(back_populates="wins")

    votes: list["Vote"] = Relationship(back_populates="match")

class MatchInfo(BaseMatchInfo):
    'match info for client side'
    players: list["BasePlayerInfo"]
    colony: "BaseColonyInfo"

# the vote system
    
class BaseVote(SQLModel):
    '''
    ### The base class for a vote
    `player_id: int = Field(foreign_key="player.id", ondelete="RESTRICT")`
    `ct_app_id: int = Field(foreign_key="ctapp.id", ondelete="RESTRICT")`

    `domain_expansion: bool = Field(default=False, description="the player's domain expansion")`
    `binding_vow: bool = Field(default=False, description="the player's binding vow")`
    `simple_domain: bool = Field(default=False, description="the player's simple domain")`
    '''
    player_id: int | None = Field(default=None, foreign_key="player.id", ondelete="RESTRICT")
    ct_app_id: int | None = Field(default=None, foreign_key="ctapp.id", ondelete="RESTRICT")

    domain_expansion: bool = Field(default=False, description="the player's domain expansion")
    binding_vow: bool = Field(default=False, description="the player's binding vow")
    simple_domain: bool = Field(default=False, description="the player's simple domain")

    
class Vote(BaseVote, table=True):
    'a vote as stored in a database'
    id: int | None = Field(default=None, primary_key=True)
    
    user_id: int | None = Field(default=None, foreign_key="user.id", ondelete="SET NULL")
    match_id : int | None = Field(default=None, foreign_key="match.id", ondelete="CASCADE")
    user: "User" = Relationship(back_populates="votes") # the user casting their votes
    
    match: Match = Relationship(back_populates="votes") # the match the vote takes place

    player: "Player" = Relationship(back_populates="votes") # the player being voted for

    ct_app: "CTApp" = Relationship(back_populates="votes") # the cursed application being voted for

    # the times are useful for know when to deactivate the techniques
    de_time: time | None = Field(default=None, description="the time a player cast their domain")
    bv_time: time | None = Field(default=None, description="the time a player cast their binding_vow")
    sd_time: time | None = Field(default=None, description="the time a player cast their simple_domain")
    
class CastVote(BaseVote):
    'model for collecting data to cast a vote'
    pass

class VoteInfo(SQLModel):
    'the vote info for client-side'
    id: int
    user: "BaseUserInfo"
    player: "BasePlayerInfo"
    ct_app: "BaseCTAppInfo"



""" 

    location_id: int = Field(foreign_key='location.id')
    location: "Location" = Relationship(back_populates="matches")
    
    
    

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