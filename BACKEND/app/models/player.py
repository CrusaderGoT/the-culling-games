#./api/models/players.py
'''module for defining the `players` `cursed technique` and `cursed technique applications` models that will be used to perform CRUD operation
on the database and will be used as schemas/response/request data in the API schema. All SQLModels'''
from sqlmodel import Field, Relationship, SQLModel
from pydantic import field_validator
from datetime import date, time
from app.models.base import (BaseMatchInfo, BasePlayer, BasePlayerInfo, BaseCT, BaseCTInfo,
                            BaseCTApp, BaseUserInfo, BaseColonyInfo, MatchPlayerLink,
                            BaseBarrierTech)
from typing import TYPE_CHECKING, Union
from decimal import Decimal
if TYPE_CHECKING:
    from app.models.user import User
    from app.models.colony import Colony
    from app.models.match import Match, Vote


# PLAYER
class Player(BasePlayer, table=True):
    'The Player as stored in the database'
    id: int | None = Field(default=None, primary_key=True)
    grade: BasePlayer.Grade = Field(default=BasePlayer.Grade.FOUR, description="the grade of a player")
    points: float = Field(default=0.0, description='the overall points of a player')
    created: date = Field(default=date.today())
    ct_id: int | None = Field(default=None, foreign_key="cursedtechnique.id", ondelete="CASCADE")
    cursed_technique: "CursedTechnique" = Relationship(back_populates="player")
    # barrier techniques are only available to player of grade 2 up, implement later.
    barrier_tech_id: int | None = Field(default=None, foreign_key="barriertech.id", ondelete="CASCADE")
    barrier_technique: Union["BarrierTech", None] = Relationship(back_populates="player")
    user_id: int | None = Field(default=None, foreign_key="user.id", ondelete="SET NULL")
    user: "User" = Relationship(back_populates="player")
    colony_id: int | None = Field(default=None, foreign_key="colony.id", ondelete="SET NULL")
    colony: "Colony" = Relationship(back_populates="players")
    matches: list["Match"] = Relationship(back_populates="players", link_model=MatchPlayerLink)
    wins: list["Match"] = Relationship(back_populates="winner")
    votes: list["Vote"] = Relationship(back_populates="player")

    @field_validator('points')
    @classmethod
    def round_points(cls, points:float):
        return round(points, 1)

class CreatePlayer(BasePlayer):
    'For creating a Player'
    pass


# CURSED TECHNIQUE   
class CursedTechnique(BaseCT, table=True):
    'The cursed Technique as stored in the DB'
    id: int | None = Field(default=None, primary_key=True)
    player: Player = Relationship(back_populates="cursed_technique", cascade_delete=True)
    applications: list["CTApp"] = Relationship(back_populates="ct")

class CreateCT(BaseCT):
    'for creating cursed technique'
    pass

# CURSED TECHNIQUE APPLICATION
class CTApp(BaseCTApp, table=True):
    'cursed technique application as stored in the database'
    id: int | None = Field(default=None, primary_key=True)
    number: int = Field(ge=1, le=5)
    ct_id: int | None = Field(default=None, foreign_key="cursedtechnique.id")
    ct: CursedTechnique = Relationship(back_populates="applications")

    votes: list["Vote"] = Relationship(back_populates="ct_app")

class CreateCTApp(BaseCTApp):
    'for creating a cursed technique application'
    pass

# Advanced tech
class BarrierTech(BaseBarrierTech, table=True):
    '''
    This is the class for any buffs to a vote.\n
    This includes, `domain expansion, simple domain, binding vow`, etc.\n
    It is called `BarrierTech` cos it sounds cool.
    '''
    id: int | None = Field(default=None, primary_key=True)
    player: "Player" = Relationship(back_populates="barrier_technique", cascade_delete=True)
    # the times are useful for know when to activate/deactivate the techniques
    de_time: time | None = Field(default=None, description="the time a player cast their domain")
    bv_time: time | None = Field(default=None, description="the time a player cast their binding_vow")
    sd_time: time | None = Field(default=None, description="the time a player cast their simple_domain")

class BarrierTechInfo(BaseBarrierTech):
    id: int

# CLIENT SIDE RESPONSE MODELS
class PlayerInfo(BasePlayerInfo):
    'Player info with cursed technique, user, and colony info'
    cursed_technique: BaseCTInfo
    barrier_technique: BarrierTechInfo | None
    colony: BaseColonyInfo | None
    user: BaseUserInfo | None
    matches: list[BaseMatchInfo]

class CTInfo(BaseCTInfo):
    'cursed technique, with player info'
    player: BasePlayerInfo

# Edit Models
class EditPlayer(SQLModel):
    'For editing a Player'
    name: str | None = None
    gender: BasePlayer.Gender | None = None
    age: int| None = Field(default=None, ge=10, le=102)
    role: str | None = None

class EditCT(SQLModel):
    'for editing a cursed technique'
    name: str | None = None
    definition: str | None = None

class EditCTApp(SQLModel):
    'for editing a cursed technique application'
    number: int = Field(ge=1, le=5)
    application: str


