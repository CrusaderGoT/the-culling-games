'''module for configurations of
1. path operation decorators args; e.g tags.
2. custom exceptions.
3. Dependecies
4. Common logic'''
from app.api.settings import app
from app.models.users import UserInfo, User
from fastapi import status, Request
from fastapi.responses import JSONResponse
from enum import Enum
from pydantic import EmailStr
# configurations goes here

# 1. EXCEPTIONS

class UserException(Exception):
    '''user custom exception; will convert the User to UserInfo'''
    def __init__(self, user:User, code:int=status.HTTP_406_NOT_ACCEPTABLE,
                 err_msg:str | dict={'msg': 'An Error Occured with this User'},) -> None:
        self.user = UserInfo.model_validate(user)
        self.err_msg = err_msg
        self.code = code

@app.exception_handler(UserException)
async def user_exception_handler(request:Request, exc:UserException):
    return JSONResponse(status_code=exc.code, content=exc.err_msg)

# 2. TAGS for openapi, used to group path operators
class Tag(str, Enum):
    'tags for path operation decorators'
    user = 'users'
    player = 'players'
    auth = 'authentication'

# Common
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