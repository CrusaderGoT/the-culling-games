#./api/models/users.py
'''module for defining the `users` models that will be used to perform CRUD operations on the database and
The models that will be used as schemas/response/request data in the API schema. All SQLModels'''
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
from datetime import date
from app.models.bases import (BaseUser, BaseUserInfo, Country, BasePlayerInfo, BaseAdminInfo)
from typing import Union, TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.players import Player
    from .matches import Vote
    from .admins import AdminUser


# write your user models here

class User(BaseUser, table=True):
    'The user as stored in the database'
    id: int | None = Field(default=None, primary_key=True)
    usernamedb: str = Field(description="username as stored in the database. lowercase",
                            index=True, unique=True)
    'username as stored in the database. lowercase'
    created: date = Field(default=date.today())
    password: str = Field(description="the user's hashed password")
    player: Union["Player", None] = Relationship(back_populates="user") # no cascade_delete, default behaviour required
    admin: Union["AdminUser", None] = Relationship(back_populates="user", cascade_delete=True)

    votes: list["Vote"] = Relationship(back_populates="user")

class CreateUser(BaseUser):
    'For creating a user'
    password: str
    confirm_password: str

class EditUser(SQLModel):
    'For editing a User'
    username: str | None = None
    email: EmailStr | None = None
    country: Country| None = None

# CLIENT SIDE RESPONSE MODELS
class UserInfo(BaseUserInfo):
    'The user info'
    player: Union["BasePlayerInfo", None] = None
    admin: Union["BaseAdminInfo", None] = None

