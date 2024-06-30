'''this module handles authentication'''
import bcrypt
from app.models.users import BaseUser
from fastapi import status
from app.settings import app
from fastapi.responses import JSONResponse
from fastapi import Request


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

#user custom exception
class UserException(Exception):
    def __init__(self, user:BaseUser, code:int=status.HTTP_406_NOT_ACCEPTABLE,
                 err_msg:dict={'msg': 'An Error Occured with this User'},) -> None:
        self.user = user
        self.err_msg = err_msg
        self.code = code

@app.exception_handler(UserException)
async def user_exception_handler(request:Request, exc:UserException):
    return JSONResponse(status_code=exc.code, content=exc.err_msg)