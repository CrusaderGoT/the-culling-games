'''module for the match routers'''
from app.utils.logic import get_players_not_in_part, colonies_with_players_available_for_part
from ..models.players import Player
from ..models.matches import Match, MatchInfo, CastVote, Vote
from fastapi import APIRouter, Depends, Query, HTTPException, status, Path, Body
from ..auth.dependencies import oauth2_scheme, admin_user
from ..utils.dependencies import session
from ..utils.logic import id_name_email, get_user
from ..utils.config import Tag
from typing import Annotated
from sqlmodel import select
from random import sample, choice
from datetime import datetime, timedelta

# write you match api routes here

router = APIRouter(
    prefix='/match',
    tags=[Tag.match],
    dependencies=[Depends(oauth2_scheme)]
)

@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=MatchInfo)
def create_match(part: Annotated[int, Query()], session: session, admin: admin_user):
    '''path operation for automatically creating a match, requires a part query.'''

    # fetch colonies that has atleast one player that hasn't fought in the specified part query
    result = colonies_with_players_available_for_part(session, part)
    if result and (colony_id := choice(result)) is not None: # list is not empty and contains int (randomly chosen)
        # Fetch players from the selected colony who have not fought in the specified part.
        players_not_in_part = get_players_not_in_part(colony_id, part, session)

        # randomly select 2 players from the colony who haven't fought in the part before.
        # if only one player is available, pair them with any other player from the colony.
        if len(players_not_in_part) == 1:
            # fetch all players in colony, excluding the single player_not in_part
            all_players_query = select(Player).where(Player.colony_id == colony_id, Player.id != players_not_in_part[0].id)
            all_players = session.exec(all_players_query).all()
            
            if not all_players: # means only one player in colony
                err_msg = f"Only one player in Colony {players_not_in_part[0].colony_id}, cannot make match. Try again or add a player to the colony"
                raise HTTPException(status.HTTP_412_PRECONDITION_FAILED, err_msg)
            else:
                player1 = players_not_in_part[0] # the only player available
                player2 = choice(all_players)  # Randomly select another player from the same colony

        else: # players available are more than 2
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
        detail=f"No colony with players who haven't fought in part {part}. Begin/Try part {part+1}. Else no player yet..."
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=detail)
    
@router.get("/all", response_model=list[MatchInfo])
def get_matches(session: session,
                offset: Annotated[int, Query(ge=0)] = 0,
                limit: Annotated[int, Query(le=30)] = 10):
    'get all matches'
    stmt = select(Match).offset(offset).limit(limit)
    result = session.exec(stmt).all()
    if result:
        return result
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"No matches yet...")
    
@router.post("/vote/{match_id}/{user_id}")
def vote(session: session, match_id: Annotated[int, Path()], user_id: id_name_email, votes: Annotated[list[CastVote], Body(min_length=1 ,max_length=5)]):
    "function for casting votes"
    # first check if match and user exists
    def match_user_exists():
        'function for check if both `match` and `user` exist. raises a HTTPException otherwise.'
        match = session.exec(
            select(Match).where(Match.id == match_id)
        ).first()
        user = get_user(session, user_id)

        if match is None: # match does't exist
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"match with id {match_id} not found")
        elif user is None: # user doesn't exists
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"match with id {match_id} not found")
        return match, user
    match, user = match_user_exists() # both match and user exist
    # check if match still ongoing
    def ongoing_match(match: Match):
        'checks if a match is still ongoing, returns false if match is over, otherwise true'
        time_now = datetime.now()
        end_time = match.end
        ongoing = time_now < end_time
        return ongoing
    print(ongoing_match(match), 'hereeeeeeeeeeeeee')
    if ongoing_match(match) == True:
        return "voted"
    else: # match has ended
        raise HTTPException(status.HTTP_304_NOT_MODIFIED, detail=f"match has ended", headers={"redirect_reason": 'match has ended'})
