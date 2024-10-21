'''module for the match routers'''
from ..models.player import Player, CTApp, BarrierTech, CursedTechnique
from ..models.match import Match, MatchInfo, CastVote, Vote
from ..models.admin import Permission
from ..models.base import ModelName
from ..models.user import User
from fastapi import APIRouter, Depends, Query, HTTPException, status, Path, Body, BackgroundTasks
from ..auth.dependencies import oauth2_scheme, admin_user, active_user
from ..utils.dependencies import session
from ..utils.logic import  get_match, ongoing_match, get_player, get_last_created_match, create_new_match, round_points
from ..utils.config import Tag, UserException
from typing import Annotated
from sqlmodel import select
from datetime import timedelta, datetime

# write you match api routes here

router = APIRouter(
    prefix='/match',
    tags=[Tag.match],
    dependencies=[Depends(oauth2_scheme)]
)

@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=MatchInfo)
def create_match(part: Annotated[int, Query()], session: session, admin: admin_user):
    '''path operation for automatically creating a match, requires a part query.'''
    # first get the permission for creating match
    permission = session.exec(
        select(Permission)
        .where(Permission.model == ModelName.match) # type: ignore
        .where(Permission.level == Permission.PermissionLevel.CREATE)
    ).first()
    if permission is not None:
        # check if admin user has permission
        if permission in admin.permissions or admin.is_superuser:
            # get the last match that was created, to check if it has ended
            last_match = get_last_created_match(session)
            if last_match is not None:
                # check if it has ended
                if ongoing_match(last_match) == True:
                    msg = f"Previous Match: ID {last_match.id}, part {last_match.part} has not ended"
                    raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, msg)
                else: # previous match has ended; create match
                    new_match = create_new_match(session, part)
                    session.add(new_match)
                    session.commit()
                    session.refresh(new_match)
                    return new_match
            else: # Not a single match have been create; Create match anyway
                new_match = create_new_match(session, part)
                session.add(new_match)
                session.commit()
                session.refresh(new_match)
                return new_match
        else: # admin doesn't have permission to create match
            raise UserException(admin.user, code=status.HTTP_401_UNAUTHORIZED, detail=f"{admin.user.username} doesn't have permission to create a match.")
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
                    .join(CursedTechnique)
                    .join(CTApp, CTApp.ct_id == CursedTechnique.id)
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
                                player.points = round_points(player.points+VOTE_POINT)  # Increment player's points
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
    
@router.post('/activate/domain/{player_id}')
def domain_expansion(player_id: Annotated[int, Path()],
                    match_id: Annotated[int, Query()],
                    current_user: active_user,
                    session: session,
                    background: BackgroundTasks):
    '''Activates the domain of a player in an ongoing match.\n
    Buffs the vote to x4 per vote.\n
    Negated by simple domain'''
    # first get the match, check if it is ongoing
    match = session.get(Match, match_id)
    player = session.get(Player, player_id)
    if player is not None:
        if match is not None:
            if player.id != current_user.player.id:
                msg = f"can not activate domain of another player"
                raise UserException(current_user, status.HTTP_406_NOT_ACCEPTABLE)
            else:
                if ongoing_match(match) == True:
                    # check if domain has been actvated before
                    # get the Barrier technique of that player for the match
                    stmt = select(BarrierTech).join(Player, Player.id == player.id).join(Match, Match.id == match.id)
                    barrier_tech = session.exec(stmt).first()
                    if barrier_tech is None: # player has no barrier technique
                        msg = f"'{player.name}' doesn't have a barrier technique, upgrade the player to grade 2, to unlock Barrier Techniques"
                        raise HTTPException(status.HTTP_428_PRECONDITION_REQUIRED, msg)
                    # has a barrier tech; check if domain is currently active
                    #modify to accout for situations where one of the is True-ish/
                    # also if de end time has passed, that means that domain should have ended but the backgroud task failed
                    elif (end_time := barrier_tech.de_end_time) and barrier_tech.domain_expansion == True:
                        if end_time <= datetime.now(): # should have ended, but backgroud task failed
                            barrier_tech = activate(barrier_tech)
                            session.add(barrier_tech)
                            session.commit()
                            session.refresh(barrier_tech)
                            # schedule background task for deactivation
                            background.add_task(deactivate_domain, barrier_tech, session)
                            return barrier_tech
                        else: # active
                            raise HTTPException(status.HTTP_409_CONFLICT, f"Domain is already active, deactivates: {round_points((barrier_tech.de_end_time - datetime.now()).total_seconds())}")
                    else: # no domain activated or no deactivation time
                        barrier_tech = activate(barrier_tech)
                        session.add(barrier_tech)
                        session.commit()
                        session.refresh(barrier_tech)
                        # schedule background task for deactivation
                        background.add_task(deactivate_domain, barrier_tech, session)
                        return barrier_tech
                else: # match has ended
                    raise HTTPException(status.HTTP_423_LOCKED, f"Match ID: {match_id}, has Ended")
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Match ID: {match_id}, does not exist.")
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Player {player_id}, does not exist.")
    
def deactivate_domain(barrier_tech: BarrierTech, session: session):
    'function for the background task of deactivating a domain'
    active = True
    while active: 
        now = datetime.now() # the current time
        # check if there is an end time for the specified barrier tech DE
        if barrier_tech.de_end_time is None:
            # deactivate domain
            barrier_tech.de_end_time = None
            barrier_tech.domain_expansion = False
            session.add(barrier_tech)
            session.commit()
            active = False
            break
        # see if time for deactivation has reached
        elif now >= barrier_tech.de_end_time:
            # deactivate domain
            barrier_tech.de_end_time = None
            barrier_tech.domain_expansion = False
            session.add(barrier_tech)
            session.commit()
            active = False
            break
        else:
            # add a time pause if deactivation time is still far
            continue # loop again
def activate(barrier_tech: BarrierTech):
    # activate domain
    barrier_tech.domain_expansion = True
    # set deactivation time
    barrier_tech.de_end_time = datetime.now() + timedelta(minutes=1)
    # deduct points
    barrier_tech.player.points = round_points(barrier_tech.player.points-10)
    return  barrier_tech
