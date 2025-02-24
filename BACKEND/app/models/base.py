'''module for creating base classes/data models for other models.
\nrules:\n
should not import any class or object directly from any other model module or a module that imports from a model module.\n
base classes defined here cannot have fields annotated with any models outside this module.\n
write attributes in class string definition, for easier understanding of their structure when imported to other files.\n
should be imported only in other model modules.\n
'''
import os
from sqlmodel import SQLModel, Field, Column, TIMESTAMP
from enum import Enum, IntEnum
from datetime import date, datetime
from pydantic import EmailStr, StringConstraints
from typing import Annotated, Union
import json
from datetime import timedelta
from pathlib import Path

# Get the base directory of the current script or project
BASE_DIR = Path(__file__).resolve().parent.parent


# write your base models here

class MatchPlayerLink(SQLModel, table=True):
    'link table model for a match and player M2M relation'
    match_id: int | None = Field(default=None, foreign_key="match.id", primary_key=True)
    player_id: int | None = Field(default=None, foreign_key="player.id", primary_key=True)
 
username_pydantic_regex = Annotated[
str, StringConstraints(strip_whitespace=True, pattern=r'^[A-Za-z][A-Za-z0-9_-]{2,19}$')
    ]
'''
username must be alpha-numeric characters,
starting with an alphabet, no spaces,
only underscore or/and dashes.\n
#### min - 3 characters; max - 20 characters
'''

# USER
class BaseUser(SQLModel):
    '''
    Base class for a user, containing common attributes.\n
    `username: str = Field(index=True, unique=True)`
    `email: EmailStr = Field(index=True, unique=True)`
    `country: str | None = None`
    '''
    username: username_pydantic_regex = Field(
        index=True, unique=True, description="the username of the user",
        schema_extra={"examples": [ "Gojo-Senpai", "username_pattern", "1AboveAll"]}
        )
    email: EmailStr = Field(index=True, unique=True, description="the email address of the user")
    country: Union["Country", None] = Field(default=None, description="the country of origin of the user", index=True)

class BaseUserInfo(BaseUser):
    '''
    Base model for user info, without player info\n
    `id: int`
    `created: date`
    '''
    id: int
    created: date = Field(description="the date the account was created")


# PLayer
class BasePlayer(SQLModel):
    '''
    The base player, without cursed technique\n
    `name: str`
    `gender: Gender`
    `age: int| None = Field(default=None, gt=0, le=102)`
    `role: str | None = None`
    '''
    class Gender(str, Enum):
        'the player gender options'
        m = "male"
        f = "female"
        nb = "non-binary"
    class Grade(IntEnum):
        'the enum class for player grades'
        SPECIAL = 0
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
    name: str = Field(index=True, min_length=2, max_length=50, nullable=False, description="The name of the player, must be between 2 and 50 characters")
    gender: Gender = Field(index=True)
    age: int = Field(ge=10, le=102, index=True)
    role: str | None = Field(default=None, min_length=3, max_length=50, description="The role of the player, e.g., doctor, lawyer, student, curse user, sorcerer etc.")

class BasePlayerInfo(BasePlayer):
    '''
    Base model for player info, without cursed technique info and user info\n
    `id: int`
    `created: date`
    `grade: BasePlayer.Grade`
    `points: Decimal`
    '''
    id: int
    created: date
    grade: BasePlayer.Grade
    points: float

# CURSED TECHNIQUE
class BaseCT(SQLModel):
    '''
    The base cursed technique
    `name: str`
    `definition: str`
    '''
    name: str = Field(min_length=3, max_length=100, description="The name of the cursed technique, must be between 3 and 100 characters", schema_extra={"examples": ["Boogie Woogie", "Cursed Speech", "Infinity", "Black Flash"]})
    definition: str = Field(min_length=50, max_length=500, description="The definition of the cursed technique, explaining what it does without including its subsets")

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
    name: str
    application: str
    '''
    name: str = Field(min_length=3, max_length=100, description="The name of the application, must be between 3 and 100 characters", schema_extra={"examples": ["Hollow Purple", "Demon Dogs", "Resonance", "Overtime"]})
    application: str = Field(min_length=100, max_length=500, description="The application of the cursed technique, explaining how it is used or applied in practice")

class BaseCTAppInfo(BaseCTApp):
    '''
    base model for cursed technique application info, without "ct_id", "ct"\n
    id: int
    number: int
    '''
    id: int
    number: int

def load_countries():
        'Load the countries into a dict, from the JSON file'
        fp = os.path.join(BASE_DIR, "models", "countries.json")
        with open(fp, 'r') as file:
            data: dict[str, str] = json.load(file)
        return data
Country = Enum("Country", load_countries())

class BaseColony(SQLModel):
    '''base class for a colony.\n
    country: Country
    '''
    country: Country 

class BaseColonyInfo(BaseColony):
    '''base colony info without matches\n
    id: int
    '''
    id: int

def load_table_names():
        'Load the table names dict from the JSON file'
        fp = os.path.join(BASE_DIR, "database", "table_names.json")
        with open(fp, 'r') as file:
            data: dict[str, str] = json.load(file)
        return data
ModelName = Enum("ModelName", load_table_names())



class BasePermission(SQLModel):
    '''the base class for a permission\n
    >>> class PermissionLevel(IntEnum):
        READ = 1
        CREATE = 2
        UPDATE = 3
        DELETE = 4
    model: ModelName = Field(description="The model the permission applies to")
    '''
    class PermissionLevel(IntEnum):
        READ = 1
        CREATE = 2
        UPDATE = 3
        DELETE = 4
    model: ModelName = Field(description="The model the permission applies to", index=True)



class BasePermissionInfo(BasePermission):
    '''base permission data, without id
    \n`name: str = Field(description="Permission name")`
    \n`level: BasePermission.PermissionLevel`'''
    name: str = Field(description="Permission name")
    level: BasePermission.PermissionLevel


class BaseAdminInfo(SQLModel):
    '''
    base admin info without the user info\n
    `is_superuser: bool | None`
    `permissions: list[BasePermissionInfo]`
    '''
    is_superuser: bool
    permissions: list[BasePermissionInfo]


class AdminPermissionLink(SQLModel, table=True):
    'the m2m link table for an admin and permission(s)'
    admin_id: int | None = Field(default=None, foreign_key="adminuser.id", primary_key=True)
    permission_id: int | None = Field(default=None, foreign_key="permission.id", primary_key=True)


class BaseMatch(SQLModel):
    """Base match model\n
    begin: datetime
    end: datetime
    part: int
    """
    begin: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True)))
    end: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True)))
    part: int


class BaseMatchInfo(BaseMatch):
    '''base match info with the `winner`, but without players and colony infos.\n
    `id: int`
    `winner: Union[BasePlayerInfo, None]`
    '''
    id: int
    winner: Union[BasePlayerInfo, None]

class BaseBarrierTech(SQLModel):
    """base class for barrier techniques\n
    domain_expansion: bool = Field(default=False, description="the player's domain expansion")
    binding_vow: bool = Field(default=False, description="the player's binding vow")
    simple_domain: bool = Field(default=False, description="the player's simple domain")
    
    #### The times are useful for know when to activate/deactivate the techniques
    de_end_time: datetime | None = Field(default=None, description="the time a player cast their domain")
    bv_end_time: datetime | None = Field(default=None, description="the time a player cast their binding_vow")
    sd_end_time: datetime | None = Field(default=None, description="the time a player cast their simple_domain")
    """
    domain_expansion: bool = Field(default=False, description="the player's domain expansion")
    binding_vow: bool = Field(default=False, description="the player's binding vow")
    simple_domain: bool = Field(default=False, description="the player's simple domain")
    
    # the times are useful for know when to activate/deactivate the techniques
    de_end_time: datetime | None = Field(default=None, sa_column=Column(TIMESTAMP(timezone=True)), description="the time a player cast their domain")
    bv_end_time: datetime | None = Field(default=None, sa_column=Column(TIMESTAMP(timezone=True)), description="the time a player cast their binding_vow")
    sd_end_time: datetime | None = Field(default=None, sa_column=Column(TIMESTAMP(timezone=True)), description="the time a player cast their simple_domain")


class BaseVote(SQLModel):
    '''
    ### The base class for a vote
    `player_id: int = Field(foreign_key="player.id", ondelete="RESTRICT")`
    `ct_app_id: int = Field(foreign_key="ctapp.id", ondelete="RESTRICT")`
    '''
    player_id: int | None = Field(default=None, foreign_key="player.id", ondelete="RESTRICT", index=True)
    ct_app_id: int | None = Field(default=None, foreign_key="ctapp.id", ondelete="RESTRICT", index=True)

class ActionTimePoint(SQLModel):
    'class for duration, limit, point, etc. of techniques, match, etc.'
    match_duration: timedelta = timedelta(minutes=10)
    domain_duration: timedelta = timedelta(minutes=5)
    simple_domain_duration: timedelta = timedelta(minutes=5)

    vote_binding_vow_limit: int = 3

    limit_binding_vow: int = 5
    limit_domain_expansion: int = 5
    limit_simple_domain: int = 5

    cost_binding_vow: float = 5.0
    cost_domain_expansion: float = 10.0
    cost_simple_domain: float = 7.0

    vote_point: float = 0.2
    domain_expansion_point:float = 4.0
    simple_domain_point:float = 2.0

    winner_point: float = 5.0

    delay_begin_match: timedelta = timedelta(seconds=60)
