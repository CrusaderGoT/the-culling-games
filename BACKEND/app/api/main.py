from sqlmodel import or_, select
from app.api.settings import app
from fastapi import Body, Depends, status, HTTPException
from app.models.user import CreateUser, User, UserInfo
from app.utils.dependencies import session
from typing import Annotated
from app.auth.credentials import PasswordAuth, authenticate_user, create_access_token
from app.auth.models import Token
from app.utils.config import Tag
from fastapi.security import  OAuth2PasswordRequestForm
from app.routers import admins, matches, players, users
from ..utils.logic import usernamedb
#from ..models.admins import AdminUser


# ROUTERS
app.include_router(users.router)
app.include_router(players.router)
app.include_router(matches.router)
app.include_router(admins.router)

# LOGIN
@app.post("/login", response_model=Token, status_code=status.HTTP_200_OK,
          tags=[Tag.auth], summary='creates a login token', response_description='A Token',
          include_in_schema = False)
def create_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                session: session):
    user = authenticate_user(usernamedb(form_data.username), form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
            )
    access_token = create_access_token(data={"usernamedb": user.usernamedb})
    return Token(access_token=access_token, token_type="Bearer")

# REGISTER
@app.post("/signup", response_model=UserInfo, status_code=status.HTTP_201_CREATED,
          tags=[Tag.user], summary='Create a new User', response_description='New User')
def create_user(session: session,
                user: Annotated[CreateUser, Body(description="The User details; Request")]):
    # convert user username to lowercase; for easier variable use
    l_username = usernamedb(user.username)
    # check if username or email already in use
    already_username_email = session.exec(
        select(User).where(
            or_(User.usernamedb == l_username,
                User.email == user.email)
        )
    ).first()
    if already_username_email: # a user with email or username exist
        # check which in username or email being used and inform client
        if already_username_email.usernamedb == l_username:
            err_msg = f"'{user.username}' is already in use."
            raise HTTPException(status.HTTP_409_CONFLICT, detail=err_msg)
        elif already_username_email.email == user.email:
            err_msg = f"'{user.email}' is already in use."
            raise HTTPException(status.HTTP_409_CONFLICT, detail=err_msg)
        else:
            err_msg = f"user with username or email already exist."
            raise HTTPException(status.HTTP_409_CONFLICT, detail=err_msg)
    else: # user not already in DATABASE
        # check if user password matches
        print(user.password, user.confirm_password)
        if user.password == user.confirm_password:
            pw_auth = PasswordAuth()
            hashed_pw = pw_auth.hash_password(user.password)
            update = {
                "password": hashed_pw, # store hashed password
                "usernamedb": l_username, # strore the usernamedb in lowercase
                #"admin": AdminUser(is_superuser=True)
            }
            new_user_db = User.model_validate(user, update=update)
            session.add(new_user_db)
            session.commit()
            session.refresh(new_user_db)
            return new_user_db
        else:
            err_msg = f"passwords do not match"
            raise HTTPException(status.HTTP_412_PRECONDITION_FAILED, detail=err_msg)

