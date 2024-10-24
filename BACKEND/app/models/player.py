#./api/models/players.py
'''module for defining the `players` `cursed technique` and `cursed technique applications` models that will be used to perform CRUD operation
on the database and will be used as schemas/response/request data in the API schema. All SQLModels'''
from sqlmodel import Field, Relationship, SQLModel
from datetime import date
from app.models.barrier import BarrierTech, BarrierTechInfo
from app.models.base import (BaseMatchInfo, BasePlayer, BasePlayerInfo, BaseCT, BaseCTInfo,
                            BaseCTApp, BaseUserInfo, BaseColonyInfo, MatchPlayerLink)
from typing import TYPE_CHECKING, Union
if TYPE_CHECKING:
    from app.models.user import User
    from app.models.colony import Colony
    from app.models.match import Match, Vote


# PLAYER
class Player(BasePlayer, table=True):
    'The Player as stored in the database'
    id: int | None = Field(default=None, primary_key=True)
    grade: BasePlayer.Grade = Field(default=BasePlayer.Grade.FOUR, description="the grade of a player", index=True)
    points: float = Field(default=0.0, description='the overall points of a player')
    created: date = Field(default=date.today(), index=True)
    # child relations
    cursed_technique: "CursedTechnique" = Relationship(back_populates="player")
    # barrier techniques are only available to player of grade 2 up, implement later.
    barrier_technique: "BarrierTech" = Relationship(back_populates="player")
    matches: list["Match"] = Relationship(back_populates="players", link_model=MatchPlayerLink)
    wins: list["Match"] = Relationship(back_populates="winner")
    votes: list["Vote"] = Relationship(back_populates="player")
    # parent relations
    user_id: int | None = Field(default=None, foreign_key="user.id", ondelete="SET NULL", index=True)
    user: "User" = Relationship(back_populates="player")
    colony_id: int | None = Field(default=None, foreign_key="colony.id", ondelete="SET NULL", index=True)
    colony: "Colony" = Relationship(back_populates="players")

class CreatePlayer(BasePlayer):
    'For creating a Player'
    pass


# CURSED TECHNIQUE   
class CursedTechnique(BaseCT, table=True):
    'The cursed Technique as stored in the DB'
    id: int | None = Field(default=None, primary_key=True)
    # parent rel
    player_id: int | None = Field(default=None, foreign_key="player.id", ondelete="CASCADE", index=True)
    player: Player = Relationship(
        back_populates="cursed_technique",
        # the following argument makes it so that if the cursed tech is deleted, the player will be deleted also
        # this is because a player must have a ct, otherwise, an error occurs when fetching the player.
        # not to be confused with the on_delete arg in player_id, which deletes a ct if the player is deleted
        sa_relationship_kwargs={
            "single_parent": True,
            "cascade": "all, delete",
        }
    )
    # child rel
    applications: list["CTApp"] = Relationship(back_populates="ct", cascade_delete=True)

class CreateCT(BaseCT):
    'for creating cursed technique'
    pass

# CURSED TECHNIQUE APPLICATION
class CTApp(BaseCTApp, table=True):
    'cursed technique application as stored in the database'
    id: int | None = Field(default=None, primary_key=True)
    number: int = Field(ge=1, le=5)
    # parent rel
    ct_id: int | None = Field(default=None, foreign_key="cursedtechnique.id", index=True, ondelete="CASCADE")
    ct: CursedTechnique = Relationship(back_populates="applications")
    # child rel
    votes: list["Vote"] = Relationship(back_populates="ct_app")

class CreateCTApp(BaseCTApp):
    'for creating a cursed technique application'
    pass

# Advanced Techniques
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


