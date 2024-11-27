'''routes for admin purposes/interface'''
from fastapi import APIRouter, status, Body, HTTPException, Query, Depends
from sqlmodel import select
from typing import Annotated
from ..models.admin import AdminUser, Permission, AdminInfo, CreatePermission, PermissionInfo
from ..utils.logic import get_user, id_name_email
from ..utils.dependencies import session
from ..utils.config import UserException, Tag
from ..auth.dependencies import admin_user
from dotenv import load_dotenv
import os

load_dotenv()

# Create your API routes here
router = APIRouter(
    prefix='/admin', tags=[Tag.admin],
    #dependencies=[Depends(admin_user)]
)


@router.post('/create/{user}', response_model=AdminInfo)
def create_admin(
    user: id_name_email,  # The user to be promoted to admin
    session: session,  # The database session
    p_admin: admin_user,  # The currently logged-in admin user (validated by dependencies)
    permissions: Annotated[list[CreatePermission], Body()]  # List of permissions to assign to the new admin
):
    '''Creates an admin user with specified permissions.'''
    
    # Fetch the user from the database
    userdb = get_user(session, user)
    
    if userdb is None:
        # Raise 404 error if the user does not exist in the database
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"User '{user}' you want to make an admin doesn't exist.")
    
    # Prevent creating admin privileges for oneself
    if userdb == p_admin.user:
        raise UserException(p_admin.user, status.HTTP_409_CONFLICT, "Cannot make yourself an admin again.")
    
    # Check if the user is already an admin
    if userdb.admin is not None:
        raise UserException(userdb, status.HTTP_417_EXPECTATION_FAILED, f"{userdb.username} is already an admin. Edit their admin profile instead.")
    
    # Initialize an empty list to hold the new permissions for the user
    new_permissions: list[Permission] = []

    # Superuser logic: unrestricted permission assignment
    if p_admin.is_superuser:
        # Superusers can assign any permissions without restrictions
        for permission in permissions:
            for level in permission.level:
                # Try to find an existing permission in the database
                try:
                    stmt = select(Permission).where(
                        Permission.model == permission.model,
                        Permission.level == level
                    )
                    perm = session.exec(stmt).one()
                except Exception:  # If the permission does not exist, create a new one
                    name = f"can_perform_{level.name}_{level.value}_operations_on_{permission.model.name}"
                    perm = Permission(
                        model=permission.model,
                        level=level,
                        name=name
                    )
                
                # Avoid duplicate permissions
                if perm.id: # pemission already exist
                    pass
                else:
                    new_permissions.append(perm)

        # Once all permissions are processed, create the new admin user
        new_admin = AdminUser(permissions=new_permissions, user=userdb)
        session.add(new_admin)
        session.commit()
        session.refresh(new_admin)
        return new_admin
    
    # Regular admin logic: restricted permission assignment based on the current admin's level
    elif p_admin:
        # Filter permissions that the current admin can assign to others
        for permission in permissions:
            for level in permission.level:
                # Check if the current admin has the permission to assign this specific permission level
                stmt = (select(Permission)
                        .join(AdminUser, AdminUser.id == p_admin.id)
                        .where(Permission.model == permission.model)
                        .where(Permission.level == level))
                
                # Add only the permissions that the current admin is authorized to assign
                perm = session.exec(stmt).first()

                if perm and perm.id not in [p.id for p in new_permissions]:
                    new_permissions.append(perm)
        
        # After filtering, check if there are valid permissions to assign
        if new_permissions:
            # Create the new admin with the filtered permissions
            new_admin = AdminUser(permissions=new_permissions, user=userdb)
            session.add(new_admin)
            session.commit()
            session.refresh(new_admin)
            return new_admin
        else:
            # Raise an error if no valid permissions were found
            err_msg = (f"{userdb.username}'s permissions are empty. "
                       f"All permissions sent cannot be granted by you '{p_admin.user.username}'.")
            raise UserException(p_admin.user, status.HTTP_406_NOT_ACCEPTABLE, detail=err_msg)
    
    # Handle any unknown errors (this block is unlikely to run but serves as a safeguard)
    raise HTTPException(status.HTTP_400_BAD_REQUEST, "An unknown error occurred while processing the request.")

@router.post("/new/permission", response_model=list[PermissionInfo])
def new_permission(admin: admin_user, permissions: Annotated[list[CreatePermission], Body()],
                      session: session):
    'for creating new permissions; only doable by a super user'
    # check if the user is a super user
    if admin.is_superuser == False:
        raise UserException(admin.user, status.HTTP_401_UNAUTHORIZED, "only super users can create permissions")
    # get any possible already existing permission
    new_permissions: list[Permission] = list()
    for permission in permissions:
        for level in permission.level:
            # Try to find an existing permission in the database
            try:
                stmt = select(Permission).where(
                    Permission.model == permission.model,
                    Permission.level == level
                )
                perm = session.exec(stmt).one()
            except Exception:  # If the permission does not exist, create a new one
                name = f"can_perform_{level.name}_{level.value}_operations_on_{permission.model.name}"
                perm = Permission(
                    model=permission.model,
                    level=level,
                    name=name
                )
            
            # Avoid duplicate permissions
            if perm.id: # pemission already exist
                pass
            else:
                new_permissions.append(perm)
    # check atleast one new perm exist
    if not new_permissions:
        raise HTTPException(status.HTTP_411_LENGTH_REQUIRED, f"no valid permission; length -> {len(new_permissions)}")
    # add new perms to session
    session.add_all(new_permissions)
    session.commit()
    for perm in new_permissions:
        session.refresh(perm)
    return new_permissions

@router.post("/superuser/{user}")
def demo_superuser(user: id_name_email, code: Annotated[str, Query(default=...)], session: session):
    # get the user
    userdb = get_user(session, user)
    CODE = os.getenv("CODE")
    if not userdb:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"user {user} not found")
    if code != CODE:
        raise HTTPException(status.HTTP_405_METHOD_NOT_ALLOWED, "invalid code")
    admin_user = AdminUser(is_superuser=True, user=userdb)
    session.add(admin_user)
    session.commit()
    session.refresh(admin_user)
    return admin_user