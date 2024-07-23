from app.api.settings import app
from fastapi import Body, Path, Query, Depends, status, HTTPException
from app.models.users import CreateUser, User, UserInfo, EditUser
from app.models.players import (Player, CreatePlayer, PlayerInfo,
                                CreateCT, CursedTechnique,
                                CTApp, CreateCTApp)
from app.models.colony import Colony, ColonyInfo
from app.utils.dependencies import session, colony
from typing import Annotated
from app.auth.credentials import PasswordAuth, authenticate_user, create_access_token, get_user
from app.auth.models import Token
from app.auth.dependencies import active_user
from app.utils.config import UserException, Tag
from sqlmodel import select, or_
from app.database.pgsql import create_db_tables
from fastapi.security import  OAuth2PasswordRequestForm


# write you path functions here.

@app.on_event('startup')
def on_start():
    create_db_tables()

# LOGIN
@app.post("/token", response_model=Token, status_code=status.HTTP_200_OK,
          tags=[Tag.auth], summary='creates a token', response_description='A Token')
def create_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                session: session):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
            )
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")

# USERS
@app.post("/create-user", response_model=UserInfo, status_code=status.HTTP_201_CREATED,
          tags=[Tag.user], summary='Create a new User', response_description='New User')
def create_user(session: session,
                user: Annotated[CreateUser, Body(description="The User details; Request")]):
    # convert user username to lowercase; for easier variable use
    l_username = user.username.lower().strip()
    # check if username or email already in use
    already_username_email = session.exec(
        select(User).where(
            or_(User.username == l_username,
                User.email == user.email)
        )
    ).first()
    if already_username_email: # a user with email or username exist
        # check which in username or email being used and inform client
        if already_username_email.username == l_username:
            err_msg = f"'{user.username}' is already in use."
            raise HTTPException(status.HTTP_409_CONFLICT, detail=err_msg)
        elif already_username_email.email == user.email:
            err_msg = f"'{user.email}' is already in use."
            raise HTTPException(status.HTTP_409_CONFLICT, detail=err_msg)
        else:
            err_msg = f"user already exist."
            raise HTTPException(status.HTTP_409_CONFLICT, detail=err_msg)
    else: # user not already in DATABASE
        # check if user password matches
        if user.password == user.confirm_password:
            pw_auth = PasswordAuth()
            hashed_pw = pw_auth.hash_password(user.password)
            update = {
                "password": hashed_pw,
                "username": l_username, # strore the username in lowercase
            }
            new_user_db = User.model_validate(user, update=update)
            session.add(new_user_db)
            session.commit()
            session.refresh(new_user_db)
            return new_user_db
        else:
            err_msg = f"passwords do not match"
            raise HTTPException(status.HTTP_412_PRECONDITION_FAILED, detail=err_msg)

@app.get("/users/me", response_model=UserInfo, response_description="A User",
         tags=[Tag.user], summary="Get the logged in user", status_code=status.HTTP_200_OK)
def current_user(current_user: active_user) -> User:
    return current_user

@app.get('/users/{user}', response_model=UserInfo, response_description="A User",
        tags=[Tag.user], summary="Get a user.", status_code=status.HTTP_200_OK)
def A_user(session: session,
           user: Annotated[int | str, Path(description="The user's Id, Username, or Email")]):
    userdb = get_user(session, user)
    if userdb:
        return userdb
    else:
        err_msg = f"User '{user}' not found."
        raise HTTPException(status.HTTP_404_NOT_FOUND, err_msg)
    
@app.patch('/edit-user/{user}', response_model=UserInfo, response_description="Edited User",
        tags=[Tag.user], summary="Edit a user.", status_code=status.HTTP_200_OK)
def edit_user(session: session,
              user: Annotated[int | str, Path(description="The user's Id, Username, or Email")],
              password: Annotated[str, Query()],
              edit_user: Annotated[EditUser, Body()]):
    userdb = get_user(session, user)
    if userdb:
        correct_pw = PasswordAuth().verify_password(password, userdb.password)
        if correct_pw:
            # get userdata, excluding unset
            edited_user_data = edit_user.model_dump(exclude_unset=True)
            edited_user = userdb.sqlmodel_update(edited_user_data)
            session.add(edited_user)
            session.commit()
            session.refresh(edited_user)
            return edited_user
        else:
            err_msg = "password is incorrect"
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, err_msg)
    else:
        err_msg = f"User ID '{user}' not found."
        raise HTTPException(status.HTTP_404_NOT_FOUND, err_msg)


# PLAYERS  
@app.post('/create-player/{user}', response_model=PlayerInfo, tags=[Tag.player],
          response_description="New Player", summary="create a new player",
          status_code=status.HTTP_201_CREATED)
def create_player(session: session, colony: colony,
                  user: Annotated[str | int, Path(description="The user's Id, Username, or Email")],
                  player: Annotated[CreatePlayer, Body()],
                  cursed_technique: Annotated[CreateCT, Body()],
                  applications: Annotated[list[CreateCTApp], Body(min_length=5, max_length=5)]
                ):
    userdb = get_user(session, user)
    if userdb:
        # check if user already has a player
        if userdb.player:
            err_msg = f"{userdb.username} already has a player '{userdb.player.name}'. Edit player instead."
            raise UserException(userdb, status.HTTP_409_CONFLICT, err_msg)
        else: # user has no player
            ct_apps_ins = [CTApp.model_validate(ct_app) for ct_app in applications] # ct app instances, for ct_ins
            update_ct = {"applications": ct_apps_ins}
            ct_ins = CursedTechnique.model_validate(cursed_technique, update=update_ct) # cursed technique instance
            update_player = {"cursed_technique": ct_ins,
                            "user": userdb, "colony": colony}
            new_player = Player.model_validate(player, update=update_player)
            session.add(new_player)
            session.commit()
            session.refresh(new_player)
            return new_player      
    else: # no user found
        err_msg = f"User '{user}' not found"
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=err_msg)

@app.get('/player/{player_id}', response_model=PlayerInfo, status_code=status.HTTP_200_OK,
         tags=[Tag.player], response_description="A Player", summary="Get a player with their ID")
def get_player(player_id: Annotated[int, Path()], session: session):
    player = session.exec(select(Player).where(Player.id == player_id)).first()
    if player:
        print(player.cursed_technique)
        return player
    else:
        err_msg = f"player ID '{player_id}' not found"
        raise HTTPException(status.HTTP_404_NOT_FOUND, err_msg)
    
@app.get("/player/colony/{player_id}", response_model=ColonyInfo, status_code=status.HTTP_200_OK,
         tags=[Tag.player], response_description="A Colony", summary="Get a player's colony")
def get_player_colony(session: session, player_id: Annotated[int, Path()]):
    colony = session.exec(
        select(Colony).join(Player).where(Player.id == player_id)
    ).one_or_none()
    if colony:
        return colony
    else: # no colony for player; means player doesn't exist
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"player with ID '{player_id}' not found.")
