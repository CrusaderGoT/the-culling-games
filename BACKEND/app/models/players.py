#./api/models/players.py
'''module for defining the `players` `cursed technique` and `cursed technique applications` models that will be used to perform CRUD operation
on the database and will be used as schemas/response/request data in the API schema. All SQLModels'''
from sqlmodel import Field, Relationship, SQLModel
from datetime import date
from app.models.bases import (BaseMatchInfo, BasePlayer, BasePlayerInfo, BaseCT, BaseCTInfo,
                              BaseCTApp, BaseUserInfo, BaseColonyInfo, MatchPlayerLink)
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.users import User
    from app.models.colonies import Colony
    from app.models.matches import Match, Vote


# PLAYER
class Player(BasePlayer, table=True):
    'The Player as stored in the database'
    id: int | None = Field(default=None, primary_key=True)
    created: date = Field(default=date.today())
    ct_id: int | None = Field(default=None, foreign_key="cursedtechnique.id", ondelete="CASCADE")
    cursed_technique: "CursedTechnique" = Relationship(back_populates="player")
    user_id: int | None = Field(default=None, foreign_key="user.id", ondelete="SET NULL")
    user: "User" = Relationship(back_populates="player")
    colony_id: int | None = Field(default=None, foreign_key="colony.id", ondelete="SET NULL")
    colony: "Colony" = Relationship(back_populates="players")
    matches: list["Match"] = Relationship(back_populates="players", link_model=MatchPlayerLink)
    wins: list["Match"] = Relationship(back_populates="winner")

    votes: list["Vote"] = Relationship(back_populates="player")

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


# CLIENT SIDE RESPONSE MODELS
class PlayerInfo(BasePlayerInfo):
    'Player info with cursed technique, user, and colony info'
    cursed_technique: BaseCTInfo
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