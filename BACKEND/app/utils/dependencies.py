'''module for defining fastapi dependencies. Typically for codes that are repeated a lot and used in path operations'''
from ..database.pgsql import engine
from sqlmodel import Session, select, func
from ..models.colony import Colony
from ..models.player import Player
from ..models.base import Country, ActionTimePoint
from random import choice
from typing import Annotated
from fastapi import Depends

# Get Session Dependency
def get_session():
    'yields a session'
    with Session(engine) as session:
        yield session

session = Annotated[Session, Depends(get_session)]
'yields a session; an alias dependency of the `get_session` function'

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
        country = choice([c for c in countries])
        colony = Colony(country=country)
        return colony

colony = Annotated[Colony, Depends(get_or_create_colony)]
'''returns a Colony with less than 10 players, or returns a new Colony.\n
An alias dependency of the `get_or_create_colony` function'''

def _atp_def():
    '''
    `ATP Default`\n
    A helper function for returning a called ActionTimePoint, i.e, `ActionTimePoint()`\n
    This helps make the atp dependency not be a query on the API side.\n
    Because as it is called, the dependency is supplied an instance of ATP,
    with default values. Otherwise(if ATP is supplied directly as a dependency)
    the API interprets it as the values have to be filled by the client.

    '''
    return ActionTimePoint()

atp = Annotated[ActionTimePoint, Depends(_atp_def)]
'''
The Action Time Point as a dependency.
'''