'''module for the match routers'''
from app.utils.logic import get_players_not_in_part, colonies_with_players_available_for_part
from ..models.player import Player, CTApp
from ..models.match import Match, MatchInfo, CastVote, Vote
from ..models.user import User
from fastapi import APIRouter, Depends, Query, HTTPException, status, Path, Body
from ..auth.dependencies import oauth2_scheme, admin_user, active_user
from ..utils.dependencies import session
from ..utils.logic import id_name_email, get_user, get_match, ongoing_match
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
    
@router.post("/vote/{match_id}")
def vote(
    session: session,
    match_id: Annotated[int, Path()],
    voter: active_user,
    votes: Annotated[list[CastVote],
                    Body(min_length=1 ,max_length=5)]
):
    "function for casting votes"
    # first check if match and user exists
    match = get_match(session, match_id)
    if match is not None:
        # check if match still ongoing
        if ongoing_match(match) == True:
            # check if user has voted before
            prev_votes = session.exec(
                select(Vote)
                .join(User, User.id == voter.id)
                .where(Vote.match_id == match_id)
            ).all()
            if len(prev_votes) == 5: # if it has exceeded 5 votes, no more votes
                raise HTTPException(status.HTTP_423_LOCKED, "vote limit reached")
            else:
                # get the players fighting, and their ct apps
                fighters_id = session.exec(
                    select(Player.id, CTApp.id)
                    .join(Player.matches)  # Joining on the matches relationship
                    .join(CTApp, CTApp.ct_id == Player.ct_id) # join on the ct app that belongs to the players
                    .where(Match.id == match.id)  # Matching the specific match
                ).all()
                vote_list: list[Vote] = list() # votes to be added and commited to session
                print(prev_votes, 'ppppppppvotes', fighters_id)
                # now iterate over the votes and cast them for correct player ct app
                for vote in votes:
                    for player_id, ct_app_id in fighters_id: # this loops runs 20 times, should be impored to only run 5 times
                        if vote.player_id == player_id and vote.ct_app_id == ct_app_id: # vote matches intended player and ct app
                            # create vote instance
                            update_vote = {"user": voter, "match": match}
                            casted = Vote.model_validate(vote, update=update_vote)
                            if (casted.ct_app_id not in [i.ct_app_id for i in vote_list] and # checks if vote already in list
                                # use prev vote to cross check any new votes to avoid duplicates
                                casted.ct_app_id not in [i.ct_app_id for i in prev_votes]
                            ):
                                vote_list.append(casted)
                            else:
                                continue # go back to top
                print(vote_list, "listttttttttt")
                session.add_all(vote_list)
                session.commit()
                [session.refresh(v) for v in vote_list]
                return vote_list

        else: # match has ended
            raise HTTPException(status.HTTP_304_NOT_MODIFIED, detail=f"match has ended", headers={"redirect_reason": 'match has ended'})
    else: # match doesn't exist
        raise HTTPException(status.HTTP_404_NOT_FOUND, "match doesn't exist")