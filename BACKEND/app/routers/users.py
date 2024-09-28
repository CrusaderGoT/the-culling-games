from app.models.user import EditUser, User, UserInfo
from app.utils.logic import get_user, get_player, id_name_email
from ..utils.config import Tag, UserException
from ..utils.dependencies import session
from ..utils.logic import usernamedb
from ..auth.dependencies import oauth2_scheme, active_user
from fastapi import APIRouter, Body, HTTPException, status, Depends
from typing import Annotated

# USERS

router = APIRouter(prefix="/users",
                   dependencies=[Depends(oauth2_scheme)],
                   tags=[Tag.user])

@router.get("/me", response_model=UserInfo, response_description="A User",
            summary="Get the logged in user", status_code=status.HTTP_200_OK)
def current_user(current_user: active_user) -> User:
    return current_user


@router.get('/{user}', response_model=UserInfo, response_description="A User",
            summary="Get a user.", status_code=status.HTTP_200_OK)
def a_user(session: session,
           user: id_name_email) -> User:
    userdb = get_user(session, user)
    if userdb:
        return userdb
    else:
        err_msg = f"User '{user}' not found."
        raise HTTPException(status.HTTP_404_NOT_FOUND, err_msg)


@router.patch('/edit/{user}', response_model=UserInfo, response_description="Edited User",
              summary="Edit a user.", status_code=status.HTTP_200_OK)
def edit_user(session: session,
              user: id_name_email,
              edit_user: Annotated[EditUser, Body()],
              current_user: active_user) -> User:
    userdb = get_user(session, user)
    if userdb:
        # check if logged in user matches user to edit
        if userdb.id != current_user.id:
            err_msg = f"User can only edit themself"
            raise UserException(current_user, status.HTTP_401_UNAUTHORIZED, err_msg)
        else:
            # get userdata, excluding unset
            edited_user_data = edit_user.model_dump(exclude_unset=True)
            # check if username was changed and update usernamedb too
            update_usernamedb = dict()
            if (username := edited_user_data.get("username")) is not None:
                update_usernamedb["usernamedb"] = usernamedb(username)
                # check if username already exists
                already_used = get_user(session, update_usernamedb["usernamedb"])
                if already_used is not None:
                    err_msg = f"'{username}' already in use."
                    raise UserException(userdb, status.HTTP_406_NOT_ACCEPTABLE, err_msg)
            # check if email was changed, and if it already exist
            if (email := edited_user_data.get("email")) is not None:
                already_used = get_user(session, email)
                if already_used is not None:
                    err_msg = f"'{email}' already in use."
                    raise UserException(userdb, status.HTTP_406_NOT_ACCEPTABLE, err_msg)
            # if all conditions have been meet, update the user
            edited_user = userdb.sqlmodel_update(edited_user_data, update=update_usernamedb)
            session.add(edited_user)
            session.commit()
            session.refresh(edited_user)
            return edited_user
    else:
        err_msg = f"User '{user}' not found."
        raise HTTPException(status.HTTP_404_NOT_FOUND, err_msg)
    
@router.delete("/delete/{user}", response_model=UserInfo, response_description="Deleted User",
               summary="Delete a user.", status_code=status.HTTP_200_OK,
               description="Deleting a user will _set null_ on the *player* if any.")
def delete_user(session: session, user: id_name_email, current_user: active_user) -> User:
    userdb = get_user(session, user)
    if userdb:
        # check that the user to be deleted is the logged in user
        if userdb.id != current_user.id:
            err_msg = "User can only delete themself" 
            raise UserException(current_user, status.HTTP_401_UNAUTHORIZED, err_msg)
        else: #logged in user matches user to be deleted
            # add user to delete session
            session.delete(userdb)
            session.commit()
            return userdb
    else:
        err_msg = f"User '{user}' not found."
        raise HTTPException(status.HTTP_404_NOT_FOUND, err_msg)