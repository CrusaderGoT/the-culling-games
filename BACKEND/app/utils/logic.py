from fastapi import Path, HTTPException, status
from typing import Annotated
from pydantic import EmailStr

from app.models.match import Match, MatchPlayerLink
from ..models.colony import Colony
from app.models.user import User
from ..models.player import Player
from app.utils.dependencies import session
from sqlmodel import Session, and_, not_, select, exists
from datetime import datetime


def usernamedb(username: str):
    'returns the username as stored in the DB -> lowercase'
    return username.lower().strip()


def is_valid_email(email: str) -> bool:
    'checks if a string is a valid email string'
    try:
        EmailStr._validate(email)
        return True
    except Exception:
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
            (4, 10),
            (3, 15),
            (2, 20),
            (1, 25),
            (0, 35),
        ]
    )
    return points_dict[grade.value]


