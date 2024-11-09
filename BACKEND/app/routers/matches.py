'''module for the match routers'''
from ..models.barrier import BarrierTech, BarrierTechInfo
from ..models.player import Player, CTApp, CursedTechnique
from ..models.match import Match, MatchInfo, CastVote, Vote
from ..models.admin import Permission
from ..models.base import ModelName
from ..models.user import User
from fastapi import APIRouter, Depends, Query, HTTPException, status, Path, Body, BackgroundTasks
from ..auth.dependencies import oauth2_scheme, admin_user, active_user
from ..utils.dependencies import session
from ..utils.config import Tag, UserException
from typing import Annotated
from sqlmodel import select
from datetime import datetime
from app.api.settings import TIME_AMT
from app.utils.logic import (
    activate_domain, deactivate_domain, get_vote_point, conditions_for_barrier_tech,
    get_match, ongoing_match, get_player, get_last_created_match, create_new_match,
    activate_simple_domain, deactivate_simple_domain)

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
    """
    function for casting votes\n
    - a match id is required
    - if an invalid vote cursed application id or player id is submitted, they are ignored.
    """
    # first check if match exists
    match = get_match(session, match_id)
    if match is not None:
        # check if match still ongoing
        if ongoing_match(match) == False:
            # check if user has voted before, and get previous votes
            prev_votes = session.exec(
                select(Vote)
                .join(User)
                .join(Match)
                .where(Vote.match_id == match_id)
                .where(User.id == voter.id)
            ).all()
            if (vote_count := len(prev_votes)) >= 5: # if it has exceeded 5 votes, no more votes
                raise HTTPException(status.HTTP_423_LOCKED, f"{vote_count} votes limit reached")
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
                    if player_id not in fighters_dict and player_id is not None:
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

                            # Add points to the player, based on barrier techniques active
                            player = get_player(session, vote.player_id)
                            if player is not None:
                                # get the opposing player, for their BT check against player
                                opposing_player = [p for p in match.players if p.id != player.id][0]
                                # get the vote point
                                vote_point = get_vote_point(match, prev_votes,
                                                            player.barrier_technique,
                                                            opposing_player.barrier_technique)
                                # Create and add the vote
                                update_vote = {"user": voter, "match": match, "point": vote_point}
                                casted_vote = Vote.model_validate(vote, update=update_vote)
                                new_votes.append(casted_vote)

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
    
@router.post('/activate/domain/{player_id}', response_model=BarrierTechInfo)
def domain_expansion(player_id: Annotated[int, Path()],
                    match_id: Annotated[int, Query()],
                    current_user: active_user,
                    session: session,
                    background: BackgroundTasks) -> BarrierTech:
    '''Activates the domain of a player in an ongoing match.\n
    Buffs the vote to x4 per vote.\n
    Weakend by simple domain'''
    # first get the match, check if it is ongoing
    match = session.get(Match, match_id)
    player = session.get(Player, player_id)

    # get the condition necessary for a BT
    barrier_tech, barrier_record, match, _ = conditions_for_barrier_tech(
        player=player, match=match, player_id=player_id,
        match_id=match_id,
        current_user=current_user, session=session)
    
    if barrier_record is not None and (count := barrier_record.domain_counter) >= TIME_AMT["DOMAIN"]:
        # check if they have reach limit for domain expansion in a match
        if ((end_time := barrier_tech.de_end_time) is not None
            and end_time <= datetime.now()
            or barrier_tech.domain_expansion == True): # should have ended, but backgroud task failed
            # deactivate domain
            deactivate_domain(barrier_tech, session)
        raise HTTPException(status.HTTP_423_LOCKED, f"domain can only be activated {count} times per match")

    elif (end_time := barrier_tech.de_end_time) and barrier_tech.domain_expansion == True:
    # has a barrier tech; check if domain is currently active
    # modify to accout for situations where one of them is True-ish/
    # also if de end time has passed, that means that domain should have ended but the backgroud task failed
        if end_time <= datetime.now(): # should have ended, but backgroud task failed
            barrier_tech = activate_domain(barrier_tech, barrier_record, match, session)
            # schedule background task for deactivation
            background.add_task(deactivate_domain, barrier_tech, session)
            return barrier_tech
        else: # active
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                f"Domain is already active, deactivates in {
                    round((barrier_tech.de_end_time - datetime.now()).total_seconds(), 1)
                } seconds."
            )
        
    else: # no domain activated or no deactivation time
        barrier_tech = activate_domain(barrier_tech, barrier_record, match, session)
        # schedule background task for deactivation
        background.add_task(deactivate_domain, barrier_tech, session)
        return barrier_tech
                    
               
    
@router.post("/activate/simple/{player_id}", response_model=BarrierTechInfo)
def simple_domain(player_id: Annotated[int, Path()],
                           match_id: Annotated[int, Query()],
                           current_user: active_user,
                           session: session,
                           background: BackgroundTasks):
    '''Activates the simple domain of a player in an ongoing match.\n
    Which either\n\t
    * Reduces the opponent's vote to half per vote, If opponent doesn't have domain expansion active.\n
    or
    * If opponent's domain is expanded, the simple domain weakens the domain expansion effect'''
    match_none = session.get(Match, match_id)
    player = session.get(Player, player_id)

    barrier_tech, barrier_record, match, _ = conditions_for_barrier_tech(
        player=player, match=match_none, player_id=player_id, match_id=match_id,
        current_user=current_user, session=session)
    
    if barrier_record is not None and (count := barrier_record.simple_domain_counter) >= TIME_AMT["SIMPLE_DOMAIN"]:
        # check if they have reached limit for simple domain in a match
        if ((end_time := barrier_tech.sd_end_time) is not None
            and end_time <= datetime.now()
            or barrier_tech.simple_domain == True): # should have ended, but backgroud task failed
            # deactivate domain
            deactivate_simple_domain(barrier_tech, session)
        raise HTTPException(status.HTTP_423_LOCKED, f"simple domain can only be activated {count} times per match")

    elif (end_time := barrier_tech.sd_end_time) and barrier_tech.simple_domain == True:
    # has a barrier tech; check if simple domain is currently active
    # modify to accout for situations where one of them is True-ish/
    # also if sd end time has passed, that means that simple domain should have ended but the backgroud task failed
        if end_time <= datetime.now(): # should have ended, but backgroud task failed
            barrier_tech = activate_simple_domain(barrier_tech, barrier_record, match, session)
            # schedule background task for deactivation
            background.add_task(deactivate_simple_domain, barrier_tech, session)
            return barrier_tech
        else: # active
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                f"Simple Domain is already active, deactivates in {
                    round((barrier_tech.sd_end_time - datetime.now()).total_seconds(), 1)
                } seconds."
            )
        
    else: # no simple domain activated or no deactivation time
        barrier_tech = activate_simple_domain(barrier_tech, barrier_record, match, session)
        # schedule background task for deactivation
        background.add_task(deactivate_simple_domain, barrier_tech, session)
        return barrier_tech


"""
# calculate match victor n=qnd
should run at the end of a match, to prevent increasing player points during a match
# add the vote points to players points
    player.points += vote_point
    # add player to session
    session.add(player)"""
