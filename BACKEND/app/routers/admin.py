'''routes for admin purposes/interface'''
from fastapi import APIRouter, status, Body
from sqlmodel import select
from typing import Annotated
from ..models.admins import AdminUser, Permission, AdminInfo, CreatePermission
from ..utils.logic import get_user, id_name_email
from ..utils.dependencies import session
from ..utils.config import UserException, Tag
from ..auth.dependencies import admin_user

# create your api routes here

router = APIRouter(prefix='/admin', tags=[Tag.admin])

@router.post('/create-admin/{user}', response_model=AdminInfo)
def create_admin(
    user: id_name_email,
    session: session,
    p_admin: admin_user,
    permisions: Annotated[list[CreatePermission], Body()]
    ):
    'for creating an admin user'
    userdb = get_user(session, user)
    if userdb is not None: # user exists
        if userdb == p_admin.user: # check if p_admin and potential new admin are the same 
            err_msg = f"cannot make yourself an admin, again."
            raise UserException(p_admin.user, status.HTTP_409_CONFLICT, err_msg)
        elif userdb.admin is not None: # check if userdb is already an admin
            err_msg = f"{userdb.username} is already an admin, edit their admin profile instead"
            raise UserException(userdb, status.HTTP_417_EXPECTATION_FAILED, detail=err_msg)
        # check if the user attempting to create an admin is a superuser or admin
        # if they are superuser, create the admin with no restrictions on permissions sent from client-side
        elif p_admin.is_superuser == True:
            # create permissions for the new admin
            new_permissions: list[Permission] = list()
            for permision in permisions:
                for level in permision.level:
                    # try and get any existing permissions first
                    try:
                        stmt = select(Permission).where(Permission.model == permision.model,
                                                        Permission.level == level)
                        perm = session.exec(stmt).one()
                    except Exception: # permission does not yet exist
                        name = f"can_perform_{level.name}_{level.value}_opreations_on_{permision.model}"
                        perm = Permission(
                            model=permision.model,
                            level=level,
                            name=name
                        )
                    if perm not in new_permissions:
                        new_permissions.append(perm)

            else: # runs after the loop to pre-create permissions
                new_admin = AdminUser(permissions=new_permissions, user=userdb)
                session.add(new_admin)
                session.commit()
                session.refresh(new_admin)
                return new_admin
            
        else: # p_admin is not a super user, but is still an admin
            # filter out permissions p_admin cannot grant to new admin
            new_permissions: list[Permission] = list()
            for permision in permisions:
                for level in permision.level:
                    stmt = (select(Permission)
                            .join(AdminUser, AdminUser.id == p_admin.id)
                            .where(Permission.model == permision.model)
                            .where(Permission.level == level)
                            )
                    perm = session.exec(stmt).first()
                    if perm and perm not in new_permissions:
                        new_permissions.append(perm)
                    else:
                        continue
            else: # runs after the loop to pre-create permissions
                if new_permissions: # some permission exists in the list
                    new_admin = AdminUser(permissions=new_permissions, user=userdb)
                    session.add(new_admin)
                    session.commit()
                    session.refresh(new_admin)
                    return new_admin
                else: # no permission in filtered list
                    err_msg = f"{userdb.username}'s permissions are empty, this is because all permissions sent, cannot be granted by you '{p_admin.user.username}'"
                    raise UserException(p_admin.user, status.HTTP_406_NOT_ACCEPTABLE, detail=err_msg)
    else: # user not in database
        return userdb