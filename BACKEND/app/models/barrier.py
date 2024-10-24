"""the module for barrier classes"""

from app.models.base import BaseBarrierTech

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.match import Match
    from app.models.player import Player

from sqlmodel import Field, Relationship, SQLModel


class BarrierTech(BaseBarrierTech, table=True):
    '''
    This is the class for any buffs to a vote.\n
    This includes, `domain expansion, simple domain, binding vow`, etc.\n
    It is called `BarrierTech` cos it sounds cool.
    '''
    id: int | None = Field(default=None, primary_key=True)
    # parent rel
    player_id: int | None = Field(default=None, foreign_key="player.id", ondelete="CASCADE")
    player: "Player" = Relationship(back_populates="barrier_technique")
    # child rel
    records: list["BarrierRecord"] = Relationship(back_populates="barrier_tech")


class BarrierRecord(SQLModel, table=True):
    'class for accounting for amount of barrier techniques used by a player during a match'

    id: int | None = Field(default=None, primary_key=True)

    domain_counter: int = Field(default=0, description="the number of times a domain is activated")
    simple_domain_counter: int = Field(default=0, description="the number of times a simple domain is activated")
    binding_vow_counter: int = Field(default=0, description="the number of times a binding vow is activated")

    # parent rel
    barrier_tech_id: int | None  = Field(default=None, foreign_key="barriertech.id", ondelete="CASCADE")
    barrier_tech: "BarrierTech" = Relationship(back_populates="records")

    match_id: int | None = Field(default=None, foreign_key="match.id", ondelete="CASCADE")
    match: "Match" = Relationship(back_populates="barrier_records")


class BarrierTechInfo(BaseBarrierTech):
    'the class for a barrier technique info'
    id: int