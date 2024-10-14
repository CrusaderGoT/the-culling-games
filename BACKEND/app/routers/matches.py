'''module for the match routers'''
from app.utils.logic import get_players_not_in_part, colonies_with_players_available_for_part
from ..models.player import Player, CTApp
from ..models.match import Match, MatchInfo, CastVote, Vote
from ..models.admin import Permission
from ..models.base import ModelName
from ..models.user import User
from fastapi import APIRouter, Depends, Query, HTTPException, status, Path, Body
from ..auth.dependencies import oauth2_scheme, admin_user, active_user
from ..utils.dependencies import session
from ..utils.logic import  get_match, ongoing_match, get_player
from ..utils.config import Tag, UserException
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
    # first get the permission
    permission = session.exec(
        select(Permission)
        .where(Permission.model == ModelName.match) # type: ignore
        .where(Permission.level == Permission.PermissionLevel.CREATE)
    ).first()
    if permission is not None:
        # check if admin user has permission
        if permission in admin.permissions or admin.is_superuser:
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
        else: # admin doesn't have permission to create match
            raise UserException(admin.user,detail=f"{admin.user.username} doesn't have permission to create a match.")
    else:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail="Permission to create a match does not exist, contact a superuser"
        )
    
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
    
@router.post("/vote/{match_id}", response_model=dict[str, list[Vote] | str])
def vote(
    session: session,
    match_id: Annotated[int, Path()],
    voter: active_user,
    votes: Annotated[list[CastVote],
                    Body(min_length=1 ,max_length=5)]
):
    """function for casting votes\n
    - a match id is required
    - if invalid vote cursed application id or player id is submitted, they are ignored.
    """
    VOTE_POINT = 0.2
    # first check if match exists
    match = get_match(session, match_id)
    if match is not None:
        # check if match still ongoing
        if ongoing_match(match) == True:
            # check if user has voted before
            prev_votes = session.exec(
                select(Vote)
                .join(User)
                .join(Match)
                .where(Vote.match_id == match_id)
                .where(User.id == voter.id)
            ).all()
            if len(prev_votes) >= 5: # if it has exceeded 5 votes, no more votes
                raise HTTPException(status.HTTP_423_LOCKED, "vote limit reached")
            else:
                # get the players fighting, and their ct apps, and store them in a dict
                fighters_dict = dict()
                for player_id, ct_app_id in session.exec(
                    select(Player.id, CTApp.id)
                    .join(Player.matches)
                    .join(CTApp, CTApp.ct_id == Player.ct_id)
                    .where(Match.id == match.id)
                ):
                    # Add ct_app_id to the corresponding player_id's list
                    if player_id not in fighters_dict:
                        fighters_dict[player_id] = []
                    fighters_dict[player_id].append(ct_app_id)

                new_votes: list[Vote] = list() # votes to be added and commited to session
                # now iterate over the votes and cast them for correct player ct app
                for vote in votes:
                    # Check if the player_id exists and if the ct_app_id is in their list of ct_app_ids
                    if (vote.player_id in fighters_dict and 
                        vote.ct_app_id in fighters_dict[vote.player_id]):
                        # Check for duplicate votes
                        if (vote.ct_app_id not in [v.ct_app_id for v in new_votes] and
                            vote.ct_app_id not in [v.ct_app_id for v in prev_votes]):
                            # Create and add the vote
                            update_vote = {"user": voter, "match": match}
                            casted_vote = Vote.model_validate(vote, update=update_vote)
                            new_votes.append(casted_vote)

                            # Add points to the player
                            player = get_player(session, vote.player_id)
                            if player is not None:
                                # check if domain is activated, blah blah blah
                                player.points += VOTE_POINT  # Increment player's points
                                session.add(player)
                else: # runs after the loop
                    session.add_all(new_votes)
                    session.commit()
                    [session.refresh(v) for v in new_votes]
                    msg = f"{len(new_votes)} out of {len(votes)} was successful"
                    info = {"message": msg, "votes": new_votes}
                    return info

        else: # match has ended
            raise HTTPException(status.HTTP_304_NOT_MODIFIED, detail=f"match has ended", headers={"redirect_reason": 'match has ended'})
    else: # match doesn't exist
        raise HTTPException(status.HTTP_404_NOT_FOUND, "match doesn't exist")