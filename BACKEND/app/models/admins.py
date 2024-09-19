#./api/models/admins.py
'''module for defining the `admin` models that will be used to perform ***special** CRUD operations on the database. All SQLModels'''
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from app.models.bases import BaseAdminInfo, BasePermission, BaseUserInfo
if TYPE_CHECKING:
    from .users import User


# write your admin models here

class AdminPermissionLink(SQLModel, table=True):
    admin_id: int | None = Field(default=None, foreign_key="adminuser.id", primary_key=True)
    permission_id: int | None = Field(default=None, foreign_key="permission.id", primary_key=True)

class AdminUser(SQLModel, table=True):
    "an admin user as stored in the database"
    id: int | None = Field(default=None, primary_key=True)
    permissions: list["Permission"] = Relationship(back_populates="admins", link_model=AdminPermissionLink)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    user: "User" = Relationship(back_populates="admin")
    is_superuser: bool = Field(default=False)

class Permission(BasePermission, table=True):
    "a permision as stored in the database"
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(description="Permission name", index=True)
    level: BasePermission.PermissionLevel = Field(description="Permission name", index=True)
    admins: list[AdminUser] = Relationship(back_populates="permissions", link_model=AdminPermissionLink)

# Model for client side
class CreatePermission(BasePermission):
    level: set[BasePermission.PermissionLevel]

class AdminInfo(BaseAdminInfo):
    'the admin info for client side'
    id: int
    user: "BaseUserInfo"
