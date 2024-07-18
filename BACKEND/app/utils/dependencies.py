'''module for defining fastapi dependencies'''
from app.database.pgsql import engine
from sqlmodel import Session, select, func
from app.models.colony import Colony
from app.models.players import Player
from app.models.bases import Country
from random import choice
from typing import Annotated
from fastapi import Depends

# Get Session Dependency
def get_session():
    'yields a session'
    with Session(engine) as session:
        yield session

session = Annotated[Session, Depends(get_session)]
'yields a session; an alias of the `get_session` function -> dependable'

def get_or_create_colony(session: session):
    '''gets a colony with less than 10 PLAYERS of creates a new base colony.
    depends on the session dependable'''
    # get a random colony to add the player
    subquery = (
        select(Colony.id, func.count(Player.id).label("player_count"))
        .join(Player, isouter=True)
        .group_by(Colony.id)
        .having(func.count(Player.id) < 10)
    ).subquery()
    colony = session.exec(
        select(Colony).where(Colony.id.in_(select(subquery.c.id)))
    ).first()
    if colony:
        return colony
    else: # return new colony instance
        # select a random country
        countries = list(Country)
        country = choice([cv.value for cv in countries])
        colony = Colony(country=country)
        return colony

colony = Annotated[Colony, Depends(get_or_create_colony)]
'''returns a Colony with less than 10 players, or returns a new BaseColony.\n
An alias of the `get_or_create_colony` function'''