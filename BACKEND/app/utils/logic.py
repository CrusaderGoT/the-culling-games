from fastapi import Path, HTTPException, status
from typing import Annotated, Literal
from email_validator import validate_email, EmailNotValidError

from app.models.barrier import BarrierRecord, BarrierTech
from app.models.match import Match, MatchPlayerLink
from ..models.colony import Colony
from app.models.user import User
from ..models.player import Player
from app.utils.dependencies import session
from sqlmodel import Session, and_, not_, select, exists
from random import sample, choice
from datetime import datetime, timedelta
import time


def usernamedb(username: str):
    'returns the username as stored in the DB -> lowercase'
    return username.lower().strip()


def is_valid_email(email: str) -> bool:
    'checks if a string is a valid email string'
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def get_match(session: session, match_id: int):
    'function for getting a match via its ID.'
    match = session.exec(
        select(Match).where(Match.id == match_id)
    ).first()
    return match

def get_user(session: session, user_name_id_email: str | int):
    '''gets a user (using id, username, or email) from the database or returns none if user not found.
    \nuser_name_id_email: `username`, `userid`, or `email`'''
    # try to convert the str to int for id
    try:
        user_id = int(user_name_id_email)
    except ValueError:
        pass
    else:
        user_name_id_email = user_id

    if isinstance(user_name_id_email, str):
        # check if it is an email str
        if is_valid_email(user_name_id_email):
            statement = select(User).where(User.email == user_name_id_email)
            user = session.exec(statement=statement).first()
            return user
        else: # a username then
            username = usernamedb(user_name_id_email)
            statement = select(User).where(User.usernamedb == username)
            user = session.exec(statement=statement).first()
            return user
    elif isinstance(user_name_id_email, int):
        user = session.get(User, user_name_id_email)
        return user
    else:
        return None
    
def get_player(session: session, player_id: int):
    'for getting a player from the database'
    player = session.get(Player, player_id)
    if player:
        return player
    else:
        return None
    
def match_user_exists(session: session, match_id: int, user_id: int | str):
        'function for check if both `match` and `user` exist. raises a HTTPException otherwise.'
        match = get_match(session, match_id)
        user = get_user(session, user_id)
        if match is None: # match does't exist
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"match with id {match_id} not found")
        elif user is None: # user doesn't exists
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"match with id {match_id} not found")
        return match, user

def get_players_not_in_part(colony_id: int, part: int, session: Session):
    """
    Fetch players from a specified colony who haven't fought in a match for the given part.
    """
    # Subquery to get player IDs who have fought in the specified part
    part_matches_subquery = (
        select(MatchPlayerLink.player_id)
        .join(Match, MatchPlayerLink.match_id == Match.id)
        .where(Match.id == part)
    )

    part_matches_select = select(part_matches_subquery.c.player_id)

    # Query to get players in the specified colony who haven't fought in the part
    players_not_in_part_query = (
        select(Player)
        .where(
            and_(
                Player.colony_id == colony_id,
                not_(Player.id.in_(part_matches_select))
            )
        )
    )

    players_not_in_part = session.exec(players_not_in_part_query).all()

    return players_not_in_part

def select_players_fought_in_part(part: int):
        '''Subquery to get player IDs who have fought in the specified part\n
        returns a select statement'''
        subquery = (
            select(MatchPlayerLink.player_id)
            .join(Match, MatchPlayerLink.match_id == Match.id)
            .where(Match.part == part)
        ).subquery(name=f"matches_in_part_{part}")
        # Convert the subquery into a select() construct for use in the IN clause
        subquery_select = select(subquery.c.player_id)
        return subquery_select

def colonies_with_players_available_for_part(session: session, part: int):
    "Main query to get colonies IDs with at least one player who hasn't fought in the specified part"
    subquery_select = select_players_fought_in_part(part=part)
    statement = select(Colony.id).where(
        exists(
            select(Player.id)
            .where(
                and_(
                    Player.colony_id == Colony.id,
                    not_(Player.id.in_(subquery_select))
                )
            )
        )
    )
    result = session.exec(statement).all()
    return result


id_name_email = Annotated[int | str, Path(description="The user's Id, Username, or Email")]
"""The user's Id, Username, or Email as a Path parameter.
\nActually accepts any int or str. The name is for convention."""

def ongoing_match(match: Match):
        'checks if a match is still ongoing, returns false if match is over, otherwise true'
        time_now = datetime.now()
        end_time = match.end
        ongoing = time_now < end_time
        return ongoing


def points_required_for_upgrade(grade: Player.Grade):
    'returns the points required for an upgrade'
    points_dict = dict(
        [
            (4, 0.2),
            (3, 0.2),
            (2, 0.4),
            (1, 0.4),
            (0, 0.6),
        ]
    )
    return points_dict[grade.value]

def get_last_created_match(session: session):
    'Get the last created Match, according to begin date. None if no Match exists'
    last_match = session.exec(
        select(Match).order_by(Match.begin.desc())
        .limit(1)
    ).first()
    return last_match

def create_new_match(session: session, part: int):
    'creates a new match, needs a lot of refactoring'
    # fetch colonies that has atleast one player that hasn't fought in the specified part query
    result = colonies_with_players_available_for_part(session, part)
    if result and (colony_id := choice(result)) is not None: # list is not empty and contains int (randomly chosen)
        # Fetch players from the selected colony who have not fought in the specified part.
        players_not_in_part = get_players_not_in_part(colony_id, part, session)
        # Randomly select 2 players from the colony for the match
        players = random_players_for_match(session, players_not_in_part, colony_id) # type: ignore ; list same as Sequence
        # create match
        begin = datetime.now() + timedelta(minutes=2)
        end = begin + timedelta(hours=24)
        new_match = Match(begin=begin, end=end, part=part,
                        colony_id=colony_id, players=players)
        return new_match
    else:
        detail=f"No colony with players who haven't fought in part {part}. Begin/Try part {part+1}. Else no player yet..."
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=detail)
    
def random_players_for_match(session: session, players_not_in_part: list[Player], colony_id: int):
    """Randomly select 2 players from the colony who haven't fought in the part before.\n
    if only one player is available, pair them with any other player from the colony.\n
    raises HTTPException if only one player in colony"""
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
    return [player1, player2]

def calculate_points(player_points: float, points_to_action: float, on_action: Literal["minus", "plus"]):
    '''
    Calculates the point needed for a player action\n
    raises a `HTTPException 428` if player points are not enough.\n
    returns a 1 decimal place | 2 precision of a float. e.g. 1.2
    '''
    # check if player points is enough
    if player_points >= points_to_action: # player has enough points
        # check which action to perform
        match on_action:
            case "plus":
                updated_points = round(player_points + points_to_action, 1)
            case "minus":
                updated_points = round(player_points - points_to_action, 1)
            case _:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "points error occured.")
        return updated_points
    else:
        msg = f"not enough points; need {points_to_action}, have {player_points}"
        raise HTTPException(status.HTTP_428_PRECONDITION_REQUIRED, detail=msg)


def activate_domain(
        barrier_tech: BarrierTech,
        barrier_record: BarrierRecord | None,
        match: Match,
        session: session):
    'function for activating a domain'
    # activate domain
    barrier_tech.domain_expansion = True
    # set deactivation time
    barrier_tech.de_end_time = datetime.now() + timedelta(minutes=1)
    # deduct points
    barrier_tech.player.points = calculate_points(barrier_tech.player.points, 10, "minus")
    # add/record the detail
    # the barrier detail should commited here
    if barrier_record is not None:
        barrier_record.domain_counter += 1
        session.add(barrier_record)
    else: # no barrier detail
        new_barrier_detail = BarrierRecord(
            domain_counter=1,
            match=match,
            barrier_tech=barrier_tech
        )
        session.add(new_barrier_detail)
    # commits
    session.add(barrier_tech)
    session.commit()
    session.refresh(barrier_tech)
    return  barrier_tech


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
            remaining_time = (barrier_tech.de_end_time - now).total_seconds()
            time.sleep(remaining_time // 2) # remaining time divide by 2
            continue # loop again