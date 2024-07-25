from sqlmodel import select, or_
from app.utils.logic import get_user, get_player
from app.models.colony import Colony, ColonyInfo
from app.models.players import (CreatePlayer, CreateCT, CreateCTApp,
                                CTApp, CursedTechnique, Player,
                                PlayerInfo, BasePlayerInfo,
                                EditPlayer, EditCT, EditCTApp)
from app.utils.config import Tag, UserException
from app.utils.dependencies import colony, session, id_name_email
from ..auth.dependencies import oauth2_scheme, active_user
from fastapi import APIRouter, Body, HTTPException, Path, status, Depends, Query
from typing import Annotated, Union

# PLAYERS 

router = APIRouter(prefix="/player",
                   dependencies=[Depends(oauth2_scheme)],
                   tags=[Tag.player])


@router.post('/create/{user}', response_model=PlayerInfo, tags=[Tag.player],
          response_description="New Player", summary="Create a new player",
          status_code=status.HTTP_201_CREATED)
def create_player(session: session, colony: colony,
                  user: id_name_email,
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
            ct_apps_ins = [CTApp.model_validate(ct_app) for ct_app in applications] # ct router instances, for ct_ins
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

@router.get("/me", response_model=PlayerInfo, status_code=status.HTTP_200_OK,
            tags=[Tag.player], response_description="A Player", summary="Get a player of the logged in user")
def my_player(session: session, current_user: active_user):
    if current_user.player and type(current_user.player.id) == int:
        player = get_player(session, current_user.player.id)
        if player:
            return player
        else:
            err_msg = f"User has no Player"
            raise UserException(current_user, status.HTTP_404_NOT_FOUND, err_msg)

@router.get('/{player_id}', response_model=PlayerInfo, status_code=status.HTTP_200_OK,
         tags=[Tag.player], response_description="A Player", summary="Get a player with their ID")
def a_player(player_id: Annotated[int, Path()], session: session):
    player = session.exec(select(Player).where(Player.id == player_id)).first()
    if player:
        print(player.cursed_technique)
        return player
    else:
        err_msg = f"player ID '{player_id}' not found"
        raise HTTPException(status.HTTP_404_NOT_FOUND, err_msg)

@router.patch('/edit/{player_id}', response_model=PlayerInfo, status_code=status.HTTP_200_OK,
              tags=[Tag.player], response_description="Edited Player", summary="Edit a player details.")
def edit_player(player_id: int, session: session, player: EditPlayer,
                cursed_technique: EditCT, applications: Annotated[list[EditCTApp], Body(max_length=5)]):
    """If an application is sent, it should have a valid number for the application you want to edit.
    \nTo check an application id, first get a player info using the '/players/{player_id} request.
    """
    playerdb = get_player(session, player_id)
    if playerdb:
        # get infos to edit
        edit_player_data = player.model_dump(exclude_unset=True)
        edit_ct_data = cursed_technique.model_dump(exclude_unset=True)
        # get the list of ct apps to from db
        ctapps = session.exec(
            select(CTApp)
            .join(CursedTechnique)
            .where(CTApp.ct_id == playerdb.ct_id)
        ).all()
        for ct_app in ctapps:
            for edit_ct_app in applications:
                if edit_ct_app.id == ct_app.id:
                    # exclude id from modeldump; don't want to changed that
                    ct_app_data = edit_ct_app.model_dump(exclude={"id"})
                    ct_app.sqlmodel_update(ct_app_data)
        # update remaining database infos
        playerdb.cursed_technique.sqlmodel_update(edit_ct_data)
        edited_player = playerdb.sqlmodel_update(edit_player_data)
        session.add(edited_player)
        session.commit()
        session.refresh(edited_player)
        return edited_player
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Player with ID {player_id} not found")

@router.delete('/delete/{player_id}', response_model=PlayerInfo)
def delete_player(player_id: int, session: session, current_user: active_user):
    playerdb = get_player(session, player_id)
    if playerdb:
        if playerdb.user_id == current_user.id: # logged in user matches players user
            session.delete(playerdb)
            session.commit()
            return playerdb
        else: # player user don't match
            err_msg = f"Attempting to delete another player."
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, err_msg)
    else:
        err_msg = f"Player with ID '{player_id}' not found"
        raise HTTPException(status.HTTP_404_NOT_FOUND, err_msg)
    
@router.get('/all/players', response_model=Union[list[PlayerInfo], list[BasePlayerInfo]])
def get_players(session: session,
                offset: Annotated[int, Query()] = 0,
                limit: Annotated[int, Query(le=30)] = 10,
                slim: Annotated[bool, Query(description="If true, minimal player info will be returned")] = True,
                gender: Annotated[Player.Gender | None, Query()] = None,
                age: Annotated[int | None, Query(ge=10, le=102)] = None,
                role: Annotated[str | None, Query()] = None
                ):
    players = session.exec(
        select(Player).offset(offset).limit(limit)
        
    )
    if slim == True:
        players = [BasePlayerInfo.model_validate(player) for player in players]
    return players