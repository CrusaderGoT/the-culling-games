from app.settings import app
from fastapi import Body, Path, Query, status, HTTPException, Depends
from app.models.users import CreateUser, User, UserInfo, EditUser
from app.models.players import (Player, CreatePlayer, PlayerInfo,
                                CreateCT, CursedTechnique,
                                CTApp, CreateCTApp)
from app.utils.dependencies import get_session
from typing import Annotated
from app.utils.auth import PasswordAuth
from app.utils.config import UserException, Tag
from sqlmodel import Session, select, or_
from app.database.pgsql import create_db_tables

# write you path functions here.

@app.on_event('startup')
def on_start():
    create_db_tables()

# USERS
@app.post("/create-user", response_model=UserInfo, status_code=status.HTTP_201_CREATED,
          tags=[Tag.user], summary='Create a new User', response_description='New User')
def create_user(session: Annotated[Session, Depends(get_session)],
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
        
@app.get('/users/{user_id}', response_model=UserInfo, response_description="A User",
        tags=[Tag.user], summary="get a user with their ID.", status_code=status.HTTP_200_OK)
def get_user(session: Annotated[Session, Depends(get_session)],
             user_id: Annotated[int, Path()]):
    user = session.exec(select(User).where(User.id == user_id)).first()
    if user:
        return user
    else:
        err_msg = f"User ID '{user_id}' not found."
        raise HTTPException(status.HTTP_404_NOT_FOUND, err_msg)
    
@app.patch('/edit-user/{user_id}', response_model=UserInfo, response_description="Edited User",
        tags=[Tag.user], summary="get a user with their ID.", status_code=status.HTTP_200_OK)
def edit_user(session: Annotated[Session, Depends(get_session)],
              user_id: Annotated[int, Path()],
              password: Annotated[str, Query()],
              edit_user: Annotated[EditUser, Body()]):
    user = session.exec(select(User).where(User.id == user_id)).first()
    if user:
        correct_pw = PasswordAuth().verify_password(password, user.password)
        if correct_pw:
            # get userdata, excluding unset
            edited_user_data = edit_user.model_dump(exclude_unset=True)
            edited_user = user.sqlmodel_update(edited_user_data)
            session.add(edited_user)
            session.commit()
            session.refresh(edited_user)
            return edited_user
        else:
            err_msg = "password is incorrect"
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, err_msg)
    else:
        err_msg = f"User ID '{user_id}' not found."
        raise HTTPException(status.HTTP_404_NOT_FOUND, err_msg)


# PLAYERS  
@app.post('/create-player/{user_id}', response_model=PlayerInfo, tags=[Tag.player],
          response_description="New Player", summary="create a new player",
          status_code=status.HTTP_201_CREATED)
def create_player(session: Annotated[Session, Depends(get_session)],
                  user_id: Annotated[str, Path()],
                  player: Annotated[CreatePlayer, Body()],
                  cursed_technique: Annotated[CreateCT, Body()],
                  applications: Annotated[list[CreateCTApp], Body(min_length=5, max_length=5)]
                ):
    user = session.get(User, user_id)
    if user:
        ct_apps_ins = [CTApp.model_validate(ct_app) for ct_app in applications] # ct application instances, for ct_ins
        update_ct = {"applications": ct_apps_ins}
        ct_ins = CursedTechnique.model_validate(cursed_technique, update=update_ct) # cursed technique instance
        update_player = {"cursed_technique": ct_ins,
                         "user": user}
        new_player = Player.model_validate(player, update=update_player)
        session.add(new_player)
        session.commit()
        session.refresh(new_player)
        return new_player
    else: # no user found
        err_msg = f"user ID '{user_id}' not found"
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=err_msg)

@app.get('/player/{player_id}', response_model=PlayerInfo, status_code=status.HTTP_200_OK,
         tags=[Tag.player], response_description="A Player", summary="Get a player with their ID")
def get_player(player_id: Annotated[int, Path()], session: Annotated[Session, Depends(get_session)]):
    player = session.exec(select(Player).where(Player.id == player_id)).first()
    if player:
        print(player.cursed_technique)
        return player
    else:
        err_msg = f"player ID '{player_id}' not found"
        raise HTTPException(status.HTTP_404_NOT_FOUND, err_msg)