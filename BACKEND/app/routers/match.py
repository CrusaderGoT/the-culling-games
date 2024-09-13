'''module for the match routers'''
from app.utils.logic import get_players_not_in_part, colonies_with_players_available_for_part
from ..models.colonies import Colony
from ..models.players import Player
from ..models.matches import Match
from ..models.matches import CreateMatch, Match, MatchPlayerLink
from fastapi import APIRouter, Depends, Query, HTTPException, status
from ..auth.dependencies import oauth2_scheme
from..utils.dependencies import session
from typing import Annotated
from sqlmodel import select
from random import sample, choice
from datetime import datetime, timedelta

# write you match api routes here

router = APIRouter(prefix='/match',
                   tags=['match'])

@router.post('/create', status_code=status.HTTP_201_CREATED)
def create_match(part: Annotated[int, Query()], session: session):
    '''path operation for creating a match, requires a part query\n
    first fetch a colony the match will be held in\n
    then get 2 players from the colony, that havent fought in that part(current hurdle)\n
    '''
    # fetch colonies that has atleast one player that hasn't fought in the specified part query
    result = colonies_with_players_available_for_part(session, part)
    if result and (colony_id := choice(result)) is not None: # list is not empty
        # Fetch players from the selected colony who have not fought in the specified part.
        players_not_in_part = get_players_not_in_part(colony_id, part, session)

        # randomly select 2 players from the colony who haven't fought in the part before.
        # if only one player is available, pair them with any other player from the colony.
        if len(players_not_in_part) == 1:
            all_players_query = select(Player).where(Player.colony_id == colony_id, Player.id != players_not_in_part[0].id)
            all_players = session.exec(all_players_query).all()
            
            if not all_players: # means only one player in colony
                raise HTTPException(404, "Only one player in colony, cannot make match.")
            
            player1 = players_not_in_part[0] # the only player available
            player2 = choice(all_players)  # Randomly select another player from the same colony
        else:
            # Randomly select two unique players from those who haven't fought in the specified part
            player1, player2 = sample(players_not_in_part, 2)
        
        # create match
        begin = datetime.now() + timedelta(minutes=2)
        end = begin + timedelta(hours=24)
        new_match = Match(begin=begin, end=end, part=part,
                        colony_id=colony_id, players=[player1, player2])
        session.add(new_match)
        session.commit()
        session.refresh(new_match)
        return new_match
    else:
        detail=f"No colony with players who haven't fought in part {part}. Begin/Try part {part+1}."
        raise HTTPException(404, detail=detail)
    
@router.get("/{match_id}", response_model=MatchInfo)
def get_match(match_id: int, session: session):
    stmt = select(Match).where(Match.id == match_id)
    result = session.exec(stmt).first()
    if result:
        return result
    else:
        raise HTTPException(404, f"No match with id {match_id} found")