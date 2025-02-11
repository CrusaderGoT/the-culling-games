'''this module handles authentication'''
import bcrypt
from datetime import datetime, timedelta, timezone
import jwt
from app.utils.dependencies import session
from app.api.settings import SECRET_KEY, ALGORITHM
from app.utils.logic import get_user

#write your credential auths here.

class PasswordAuth:
    '''
    The Password Authentication class
    '''
    def __init__(self, salt_rounds=12):
        """
        Initialize the PasswordAuth class.

        :param salt_rounds: The number of rounds to use for salting (default: 12)
        """
        self.salt_rounds = salt_rounds

    def hash_password(self, password: str) -> str:
        """
        Hash a password string using bcrypt.

        :param password: The plaintext password to hash
        :return: The hashed password
        """
        # Generate a salt
        salt = bcrypt.gensalt(rounds=self.salt_rounds)
        # Hash the password
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verify_password(self, password: str, hashed: str) -> bool:
        """
        Verify if a password matches its hash.

        :param password: The plaintext password to verify
        :param hashed: The hashed password to compare against
        :return: True if the password matches the hash, False otherwise
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


ACCESS_TOKEN_EXPIRE_MINUTES = 10
'constant for expiration of access token'

def create_access_token(data: dict,
                        expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    '''creates an access token.
    \n`expires_delta` default `ACCESS_TOKEN_EXPIRE_MINUTES` is 60mins'''
    to_encode = data.copy()
    expires = datetime.now(timezone.utc) + expires_delta
    expires_iso = expires.isoformat() # to make json serializable
    to_encode.update({"exp": expires_iso})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(username: str, password: str, session: session):
    '''Authenticates a user using their username and password.
    \nReturns a User if authenticated, else False'''
    user = get_user(session, username)
    if not user:
        return False
    correct_pw = PasswordAuth().verify_password(password, user.password)
    if not correct_pw:
        return False
    return user
