from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from app.auth.models import TokenData
from app.api.settings import SECRET_KEY, ALGORITHM
from app.utils.logic import get_user
from app.models.users import User
from app.utils.dependencies import session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
'''A dependency of the OAuth2PasswordBearer class.'''

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                     session: session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usernamedb = payload.get("usernamedb")
        if usernamedb is None:
            raise credentials_exception
        token_data = TokenData(username=usernamedb)
    except InvalidTokenError:
        raise credentials_exception
    else:
        user = get_user(session, token_data.username)
        if user is None:
            raise credentials_exception
        return user
    
active_user = Annotated[User, Depends(get_current_user)]
'''returns the logged in user.\n
An alias dependency of the `get_current_user` function.'''