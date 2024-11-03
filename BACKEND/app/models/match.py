#./api/models/match.py
'''module for defining the `match` `location` and `vote` models that will be used to perform CRUD operation
on the database and will be used as schemas/response/request data in the API schema. All SQLModels'''
from sqlmodel import Field, Relationship, SQLModel
from ..models.barrier import BarrierRecord
from ..models.base import (BaseMatch, BaseMatchInfo, BaseVote, MatchPlayerLink,
                             BaseColonyInfo, BasePlayerInfo, BaseUserInfo,
                             BaseCTAppInfo)
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..models.player import Player, CTApp
    from ..models.colony import Colony
    from .user import User

# MATCH
class Match(BaseMatch, table=True):
    'a match as stored in the database'
    id: int | None = Field(default=None, primary_key=True)
    # parent rel
    colony_id: int | None = Field(foreign_key='colony.id', index=True, ondelete="RESTRICT")
    colony: "Colony" = Relationship(back_populates="matches")
    winner_id: int | None = Field(default=None, ondelete="RESTRICT", foreign_key='player.id', index=True, description="The winner of the match ID (player Id)")
    winner: "Player" = Relationship(back_populates="wins")
    # child rels
    #typically will have only two unique players in a match
    players: list["Player"] = Relationship(back_populates="matches", link_model=MatchPlayerLink)
    votes: list["Vote"] = Relationship(back_populates="match")
    barrier_records: list["BarrierRecord"] = Relationship(back_populates="match")
    
class MatchInfo(BaseMatchInfo):
    'match info for client side'
    players: list["BasePlayerInfo"]
    colony: "BaseColonyInfo"

# the vote system
    
class Vote(BaseVote, table=True):
    'a vote as stored in a database'
    id: int | None = Field(default=None, primary_key=True)
    
    user_id: int | None = Field(default=None, foreign_key="user.id", ondelete="SET NULL", index=True)
    match_id : int | None = Field(default=None, foreign_key="match.id", ondelete="CASCADE", index=True)
    user: "User" = Relationship(back_populates="votes") # the user casting their votes
    
    match: Match = Relationship(back_populates="votes") # the match the vote takes place

    player: "Player" = Relationship(back_populates="votes") # the player being voted for

    ct_app: "CTApp" = Relationship(back_populates="votes") # the cursed application being voted for

    point: float = Field(description="the point a vote carries")

    has_been_added: bool = Field(default=False, description="whether or not the vote point has been added to a player's point")

class CastVote(SQLModel):
    'model for collecting data to cast a vote'
    player_id: int
    ct_app_id: int

class VoteInfo(SQLModel):
    'the vote info for client-side'
    id: int
    user: "BaseUserInfo" = Field(description='the user that casted their votes')
    player: "BasePlayerInfo" = Field(description='the player voted')
    ct_app: "BaseCTAppInfo" = Field(description="the player's cursed technique application voted")
    point: float
    has_been_added: bool

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