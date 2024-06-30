from app.settings import app
from fastapi import Body, Path, File, Query, UploadFile, status, HTTPException
from app.models.users import CreateUser, User, UserInfo, UserUpdate
from app.models.players import Player, BasePlayer, PlayerInfo, CursedTechnique
# import sql_engine after all models are import
from app.database.pgsql import sql_engine
from typing import Annotated, Any
from app.utils.auth import PasswordAuth, UserException
from sqlmodel import Session, select
from datetime import datetime

# activate the sql engine
engine = sql_engine()

# write you method functions here.

@app.post("/create_user", response_model=UserInfo, response_model_exclude_unset=True,
            status_code=status.HTTP_201_CREATED)
def create_user(user: Annotated[CreateUser, Body(embed=True)]) -> UserInfo:
    '''For creating a user; uses the CreateUser class as a Body,
    and Returns a UserInfo if successful.'''
    if user.password == user.confirm_password:
        pw_auth = PasswordAuth()
        hashed_pw = pw_auth.hash_password(user.password)
        # create new_user; update password and created date/save username as lowercase to avoid cases duplication
        update = dict(password=hashed_pw, created=datetime.now().date(),
                      username=user.username.lower().strip())
        new_user = User.model_validate(user, update=update)
        # save to the database; create a session
        with Session(engine) as session:
            # add new_user to session
            session.add(new_user)
            # commit session
            session.commit()
            # refresh obj from db, else obj will be empty/expired
            session.refresh(new_user)
            # return client side data;
            return UserInfo.model_validate(new_user)
    elif user.password != user.confirm_password:
        msg = {'msg': 'passwords do not match',
                   'user': user.model_dump()}
        raise UserException(user, code=status.HTTP_409_CONFLICT, err_msg=msg)
    else:
        raise UserException(user)

@app.get('/users/me')
def current_user():
    'for getting the current user.'
    pass

@app.get('/users/{user_id_name}')
def a_user(user_id_name: Annotated[int | str, Path(description='The Username or ID',
                                               example='eg. CrusaderGoT or 1',)]) -> UserInfo:
    'for getting a specific user.'
    # try to convert user_id_name to an int
    try:
        user_id = int(user_id_name)
    except ValueError: # not convertible to an int
        # make user_id_name that is str to lowercase, becos it is stored in DB as such
        user_id_name = str(user_id_name).lower()
    else:
        user_id_name = user_id
    # create session to fetch user
    with Session(engine) as session:
        # get user if user_id_name is ID/Int
        if isinstance(user_id_name, int):
            user = session.get(User, user_id_name)
            if user: # user with id exists
                return UserInfo.model_validate(user)
            else:
                msg = f"No user with ID '{user_id_name}' Found."
                raise HTTPException(404, detail=msg)
        # get user if user_id_name is USERNAME/str
        if isinstance(user_id_name, str):
            statement = select(User).where(User.username == user_id_name)
            # get the first user, since username is unique, should typically be one
            user = session.exec(statement).first()
            if user:
                return UserInfo.model_validate(user)
            else: # no user with uername
                msg = f"No user with USERNAME '{user_id_name}' Found."
                raise HTTPException(404, detail=msg)
            
@app.patch('/edit-user/{user_id_name}')
def edit_user(user_id_name: Annotated[int | str, Path(description="The Username or UserId")],
              user: UserUpdate) -> UserInfo:
    'for updating a user info'
    # try converting user_id_name to int
    try:
        userid = int(user_id_name)
    except ValueError:
        # make user_id_name that is str to lowercase, becos it is stored in DB as such
        user_id_name = str(user_id_name).lower()
    else:
        user_id_name = userid
    # fetch user from database
    with Session(engine) as session:
        if isinstance(user_id_name, int):
            db_user = session.get(User, user_id_name)
            if not db_user:
                msg = {"error_msg": f"no user with id {user_id_name}"}
                raise HTTPException(status.HTTP_404_NOT_FOUND, detail=msg)
            else: #update user
                updated_user = user.model_dump(exclude_unset=True)
                db_user.sqlmodel_update(updated_user)
                session.add(db_user)
                session.commit()
                session.refresh(db_user)
                return UserInfo.model_validate(db_user)
        elif isinstance(user_id_name, str):
            statement = select(User).where(User.username == user_id_name)
            db_user = session.exec(statement).first()
            if not db_user:
                msg = {"error_msg": f"no user with name {user_id_name}"}
                raise HTTPException(status.HTTP_404_NOT_FOUND, detail=msg)
            else: #update user
                updated_user = user.model_dump(exclude_unset=True)
                db_user.sqlmodel_update(updated_user)
                session.add(db_user)
                session.commit()
                session.refresh(db_user)
                return UserInfo.model_validate(db_user)
        else:
            msg = {"error_msg": f"make sure 'user_id_name' is a valid string or integer"}
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=msg)

@app.delete('/delete-user/{user_id_name}')
def delete_user(user_id_name: Annotated[int | str, Path(description="The Username or UserId")],
                q: Annotated[str, Query(description='The password of the user')]) -> dict[str, Any]:
    'function for deleting a user; Any associated Player will also be delete'
    # try converting user_id_name to int
    try:
        user_id = int(user_id_name)
    except ValueError: # not convertible to an int
        # make user_id_name that is str to lowercase, becos it is stored in DB as such
        user_id_name = str(user_id_name).lower()
    else:
        user_id_name = user_id
    # get user from database; start session
    with Session(engine) as session:
        if isinstance(user_id_name, int):
            db_user = session.get(User, user_id_name)
            if db_user is not None:
                # check if q(password) matches that of the user
                pw_auth = PasswordAuth()
                correct_pw = pw_auth.verify_password(q, db_user.password)
                if correct_pw:
                    # get the player associated with the user
                    statement = select(Player).join(User)
                    player = session.exec(statement).first()
                    if player is not None: # delete player
                        session.delete(player)
                    # delete user
                    session.delete(db_user)
                    session.commit()
                    # filter user info to send to client-side
                    user_out = UserInfo.model_validate(db_user)
                    # send deleted user and if player data
                    response = dict(user=user_out, player=player)
                    msg = {"ok": True, "info": response}
                    return msg
                else:
                    msg = {'ok': False, "info": f"password does not match {db_user.username}'s password."}
                    raise UserException(db_user, status.HTTP_409_CONFLICT, err_msg=msg)
            else: # no user found
                msg = {"error_msg": f"no user with id '{user_id_name}'"}
                raise HTTPException(status.HTTP_404_NOT_FOUND, detail=msg)
        elif isinstance(user_id_name, str):
            # get user and player associated
            statement = select(User, Player).join(Player, isouter=True).where(User.username == user_id_name)
            result = session.exec(statement)
            for user, player in result:
                if user is not None: # delete user
                    # check if q(password) matches that of the user
                    pw_auth = PasswordAuth()
                    correct_pw = pw_auth.verify_password(q, user.password)
                    if correct_pw:
                        session.delete(user)
                        if player is not None: # delete player
                            session.delete(player)
                        session.commit()
                        # filter user info to send to client-side
                        user_out = UserInfo.model_validate(user)
                        response = dict(user=user_out, player=player)
                        msg = {"ok": True, "deleted": response}
                        return msg
                    else:
                        msg = {'ok': False, "info": f"password does not match {user.username}'s password."}
                        raise UserException(user, status.HTTP_409_CONFLICT, err_msg=msg)
            else:
                msg = {"error_msg": f"no user with name '{user_id_name}'"}
                raise HTTPException(status.HTTP_404_NOT_FOUND, detail=msg)



@app.post('/create-player/{username}', response_model_exclude_unset=True,
          status_code=201)
def create_player(username: Annotated[str, Path(description='The Username.')],
                  player: Annotated[Player, Body()],
                  ct: Annotated[CursedTechnique, Body(description="The Cursed Technique")]) -> dict[str, PlayerInfo | CursedTechnique]:
    '''For creating a player. Takes a user(username) in the path.
    Requires the Player and the CursedTechnique Body.'''
    # fetch the user from database
    with Session(engine) as session:
        statement = select(User).where(User.username == username.lower().strip())
        db_user = session.exec(statement).first() # get the first, since username is unique
        if db_user: # create player and cursed technique if user exists
            update = {"user_id": db_user.id}
            new_player = Player.model_validate(player, update=update)
            session.add(new_player)
            new_ct = CursedTechnique.model_validate(ct)
            session.commit()
            session.refresh(new_player)
            session.refresh(new_ct)
            response = dict(player=PlayerInfo.model_validate(new_player),
                            cursed_technique=new_ct)
            return response
        else:
            msg = f'User with username "{username}" does not exist.'
            raise HTTPException(404, detail=msg)


@app.get('/players/{player_id}')
def get_player(player_id: Annotated[int, Path(title='The player ID')]) -> dict:
    print(player_db)
    player = [player for player in player_db if player.id == player_id]
    if not player:
        return {'message': f'no player with ID -> {player_id}'}
    else:
        player_out = BasePlayer.model_construct(**player[0].model_dump())
        ct = player[0].model_dump()
        ct_out = ct['cursed_technique']
        return dict(player=player_out, cursed_technique=ct_out)

@app.post('/files')
async def upload_file(file: Annotated[bytes, File()],
                bfile: UploadFile):
    size = len(file) / 1024
    bfile.content_type
    return bfile