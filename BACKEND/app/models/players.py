#./api/models/players.py
'''module for defining the `players` models that will be used to perform CRUD operation
on the database and will be used as schemas/response/request data in the API schema. All SQLModels'''
from sqlmodel import Field, Relationship
from datetime import date
from app.models.bases import *
from typing import TYPE_CHECKING, Union
if TYPE_CHECKING:
    from app.models.users import User
    from app.models.colony import Colony, Match, MatchPlayerLink


# PLAYER
class Player(BasePlayer, table=True):
    'The Player as stored in the database'
    id: int | None = Field(default=None, primary_key=True)
    created: date = Field(default=date.today())
    ct_id: int | None = Field(default=None, foreign_key="cursedtechnique.id")
    cursed_technique: "CursedTechnique" = Relationship(back_populates="player")
    user_id: int | None = Field(default=None, foreign_key="user.id")
    user: "User" = Relationship(back_populates="player")
    colony_id: int | None = Field(default=None, foreign_key="colony.id")
    colony: "Colony" = Relationship(back_populates="players")

class CreatePlayer(BasePlayer):
    'For creating a Player'
    pass


# CURSED TECHNIQUE   
class CursedTechnique(BaseCT, table=True):
    'The cursed Technique as stored in the DB'
    id: int | None = Field(default=None, primary_key=True)
    player: Player = Relationship(back_populates="cursed_technique")
    applications: list["CTApp"] = Relationship(back_populates="ct")

class CreateCT(BaseCT):
    'for creating cursed technique'
    pass


# CURSED TECHNIQUE APPLICATION
class CTApp(BaseCTApp, table=True):
    'cursed technique application as stored in the database'
    id: int | None = Field(default=None, primary_key=True)
    ct_id: int | None = Field(default=None, foreign_key="cursedtechnique.id")
    ct: CursedTechnique = Relationship(back_populates="applications")

class CreateCTApp(BaseCTApp):
    'for creating a cursed technique application'
    pass


# CLIENT SIDE RESPONSE MODELS
class PlayerInfo(BasePlayerInfo):
    'Player info with cursed technique, user, and colony info'
    cursed_technique: BaseCTInfo
    colony: BaseColonyInfo
    user: BaseUserInfo

class CTInfo(BaseCTInfo):
    'cursed technique, with player info'
    player: BasePlayerInfo