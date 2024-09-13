'''module for defining the admin models'''
from sqlmodel import SQLModel, Field, Relationship
from enum import IntEnum
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .users import User

class SuperUser(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="superuser")

class AdminPermissionLink(SQLModel, table=True):
    admin_id: int | None = Field(foreign_key="adminuser.id", primary_key=True)
    permission_id: int | None = Field(foreign_key="permission.id", primary_key=True)

class AdminUser(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="admin")
    permissions: list["Permission"] = Relationship(back_populates="admins", link_model=AdminPermissionLink)

class Permission(SQLModel, table=True):
    class PermissionLevel(IntEnum):
        READ = 1
        CREATE = 2
        UPDATE = 3
        DELETE = 4
        ALL = 5
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(description="Permission name")
    level: PermissionLevel = Field(default=PermissionLevel.READ)
    model: str = Field(description="Model the permission applies to")
    admins: list["AdminUser"] = Relationship(back_populates="permissions", link_model=AdminPermissionLink)

class AdminInfo(SQLModel):
    id: int
    permissions: list["PermissionInfo"]

class PermissionInfo(SQLModel):
    name: str
    level: Permission.PermissionLevel
    model: str
    