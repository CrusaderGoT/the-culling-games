#./api/models/users.py
'''module for defining the `users` models that will be used to perform CRUD operations on the database and
The models that will be used as schemas/response/request data in the API schema. All SQLModels'''
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr, StringConstraints, ValidationInfo, field_validator
from datetime import date
from ..models.base import (BaseUser, BaseUserInfo, Country, BasePlayerInfo, BaseAdminInfo)
from typing import Union, TYPE_CHECKING, Annotated
from enum import Enum
from .base import username_pydantic_regex
if TYPE_CHECKING:
    from ..models.player import Player
    from .match import Vote
    from .admin import AdminUser


# write your user models here

class User(BaseUser, table=True):
    'The user as stored in the database'
    id: int | None = Field(default=None, primary_key=True)
    usernamedb: str = Field(description="username as stored in the database. lowercase",
                            index=True, unique=True)
    'username as stored in the database. lowercase'
    created: date = Field(default=date.today())
    password: str = Field(description="the user's hashed password")
    # child rel
    player: "Player" = Relationship(back_populates="user")
    admin: "AdminUser" = Relationship(
        back_populates="user", cascade_delete=True,
        # the following arg makes it so if you delete an admin the user is delete also
        sa_relationship_kwargs={
            "single_parent": True,
            "cascade": "all, delete"
        }
    )
    votes: list["Vote"] = Relationship(back_populates="user")
    #logs: list["UserLog"] = Relationship(back_populates="user", cascade_delete=True)

class CreateUser(BaseUser):
    'For creating a user'
    password: Annotated[
        str, StringConstraints(
            pattern=r"^([A-Z])([A-Za-z\d@$!%*?&\S]{7,})$")
        ] = Field(description="the user's password")
    confirm_password: Annotated[
        str, StringConstraints(
            pattern=r"^([A-Z])([A-Za-z\d@$!%*?&\S]{7,})$")
        ] = Field(description="the user's password")
    
    # Ensure password and confirm_password match
    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, confirm_password: str, valid_info:ValidationInfo):
            if confirm_password != valid_info.data.get("password"):
                raise ValueError("passwords do not match".title())
            return confirm_password

class EditUser(SQLModel):
    'For editing a User'
    username: username_pydantic_regex | None = None
    email: EmailStr | None = None
    country: Country| None = None

# CLIENT SIDE RESPONSE MODELS
class UserInfo(BaseUserInfo):
    'The user info'
    player: Union["BasePlayerInfo", None] = None
    admin: Union["BaseAdminInfo", None] = None

class UserLog(SQLModel):
    'the log model for users'
    class Method(str, Enum):
        get = "GET"
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(ondelete="CASCADE", foreign_key="user.id")
    user: User = Relationship(back_populates="logs")
    method: Method = Field(description="the http method used by the user")
    # continue tommorow