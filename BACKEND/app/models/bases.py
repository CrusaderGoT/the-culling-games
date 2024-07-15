'''module for creating base classes/data models for other models.
\nrules:\n
should not import any class or object directly from any other model module.\n
base classes defined here cannot have fields annotated with any models outside this module.\n
write attributes in string definition, for easier understanding of their structure when imported to other files.\n
should be imported only in other model modules.\n
'''
from sqlmodel import SQLModel, Field
from enum import Enum
from datetime import date
from pydantic import EmailStr

# write your base models here

# USER
class BaseUser(SQLModel):
    '''
    Base class for a user, containing common attributes.\n
    username: str = Field(index=True, unique=True)
    email: EmailStr = Field(index=True, unique=True)
    country: str | None = None
    '''
    username: str = Field(index=True, unique=True)
    email: EmailStr = Field(index=True, unique=True)
    country: str | None = None

class BaseUserInfo(BaseUser):
    '''
    Base model for user info, without player info\n
    id: int
    created: date
    '''
    id: int
    created: date


# PLayer
class BasePlayer(SQLModel):
    '''
    The base player, without cursed technique\n
    name: str
    gender: Gender
    age: int| None = Field(default=None, gt=0, le=102)
    role: str | None = None
    '''
    class Gender(str, Enum):
        'the player gender options'
        m = "male"
        f = "female"
        nb = "non-binary"
    name: str
    gender: Gender
    age: int | None = Field(default=None, gt=0, le=102)
    role: str | None = None

class BasePlayerInfo(BasePlayer):
    '''
    Base model for player info, without cursed technique info\n
    id: int
    created: date
    '''
    id: int
    created: date

# CURSED TECHNIQUE
class BaseCT(SQLModel):
    '''
    The base cursed technique
    name: str
    definition: str
    '''
    name: str
    definition: str

class BaseCTInfo(BaseCT):
    '''
    base model for ct info, without player info\n
    id: int
    applications: list["BaseCTAppInfo"]
    '''
    id: int
    applications: list["BaseCTAppInfo"]

# CURSED TECHNIQUE APPLICATION
class BaseCTApp(SQLModel):
    '''
    base model for the cursed technique application\n
    application: str
    '''
    application: str

class BaseCTAppInfo(BaseCTApp):
    '''
    base model for cursed technique application info, without "id", "ct_id", "ct"\n
    pass
    '''
    pass