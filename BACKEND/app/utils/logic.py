from pydantic import EmailStr

from app.models.users import User
from ..models.players import Player
from app.utils.dependencies import session
from sqlmodel import select


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
            statement = select(User).where(User.username == username)
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