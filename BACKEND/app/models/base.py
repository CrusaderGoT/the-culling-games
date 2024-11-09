'''module for creating base classes/data models for other models.
\nrules:\n
should not import any class or object directly from any other model module or a module that imports from a model module.\n
base classes defined here cannot have fields annotated with any models outside this module.\n
write attributes in class string definition, for easier understanding of their structure when imported to other files.\n
should be imported only in other model modules.\n
'''
from sqlmodel import SQLModel, Field
from enum import Enum, IntEnum
from datetime import date, datetime
from pydantic import EmailStr, StringConstraints
from typing import Annotated, Union
import json


# write your base models here

class MatchPlayerLink(SQLModel, table=True):
    'link table model for a match and player M2M relation'
    match_id: int | None = Field(default=None, foreign_key="match.id", primary_key=True)
    player_id: int | None = Field(default=None, foreign_key="player.id", primary_key=True)
 
username_pydantic_regex = Annotated[
        str, StringConstraints(strip_whitespace=True, pattern=r'^[a-zA-Z0-9_-]{3,20}$')
    ]
'username must be alpha-numeric characters, no spaces, only underscore or/and dashes.'

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
    name: str = Field(index=True)
    gender: Gender = Field(index=True)
    age: int | None = Field(default=None, ge=10, le=102, index=True)
    role: str | None = Field(default=None, index=True)

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
    base model for cursed technique application info, without "ct_id", "ct"\n
    id: int
    number: int
    '''
    id: int
    number: int

class Country(str, Enum):
    'the countries enum class'
    AFGHANISTAN = "AF"
    ALBANIA = "AL"
    ALGERIA = "DZ"
    ANDORRA = "AD"
    ANGOLA = "AO"
    ANTIGUA_AND_BARBUDA = "AG"
    ARGENTINA = "AR"
    ARMENIA = "AM"
    AUSTRALIA = "AU"
    AUSTRIA = "AT"
    AZERBAIJAN = "AZ"
    BAHAMAS = "BS"
    BAHRAIN = "BH"
    BANGLADESH = "BD"
    BARBADOS = "BB"
    BELARUS = "BY"
    BELGIUM = "BE"
    BELIZE = "BZ"
    BENIN = "BJ"
    BHUTAN = "BT"
    BOLIVIA = "BO"
    BOSNIA_AND_HERZEGOVINA = "BA"
    BOTSWANA = "BW"
    BRAZIL = "BR"
    BRUNEI = "BN"
    BULGARIA = "BG"
    BURKINA_FASO = "BF"
    BURUNDI = "BI"
    CABO_VERDE = "CV"
    CAMBODIA = "KH"
    CAMEROON = "CM"
    CANADA = "CA"
    CENTRAL_AFRICAN_REPUBLIC = "CF"
    CHAD = "TD"
    CHILE = "CL"
    CHINA = "CN"
    COLOMBIA = "CO"
    COMOROS = "KM"
    CONGO_DEMOCRATIC_REPUBLIC = "CD"
    CONGO_REPUBLIC = "CG"
    COSTA_RICA = "CR"
    CROATIA = "HR"
    CUBA = "CU"
    CYPRUS = "CY"
    CZECH_REPUBLIC = "CZ"
    DENMARK = "DK"
    DJIBOUTI = "DJ"
    DOMINICA = "DM"
    DOMINICAN_REPUBLIC = "DO"
    ECUADOR = "EC"
    EGYPT = "EG"
    EL_SALVADOR = "SV"
    EQUATORIAL_GUINEA = "GQ"
    ERITREA = "ER"
    ESTONIA = "EE"
    ESWATINI = "SZ"
    ETHIOPIA = "ET"
    FIJI = "FJ"
    FINLAND = "FI"
    FRANCE = "FR"
    GABON = "GA"
    GAMBIA = "GM"
    GEORGIA = "GE"
    GERMANY = "DE"
    GHANA = "GH"
    GREECE = "GR"
    GRENADA = "GD"
    GUATEMALA = "GT"
    GUINEA = "GN"
    GUINEA_BISSAU = "GW"
    GUYANA = "GY"
    HAITI = "HT"
    HONDURAS = "HN"
    HUNGARY = "HU"
    ICELAND = "IS"
    INDIA = "IN"
    INDONESIA = "ID"
    IRAN = "IR"
    IRAQ = "IQ"
    IRELAND = "IE"
    ISRAEL = "IL"
    ITALY = "IT"
    JAMAICA = "JM"
    JAPAN = "JP"
    JORDAN = "JO"
    KAZAKHSTAN = "KZ"
    KENYA = "KE"
    KIRIBATI = "KI"
    KOREA_NORTH = "KP"
    KOREA_SOUTH = "KR"
    KOSOVO = "XK"
    KUWAIT = "KW"
    KYRGYZSTAN = "KG"
    LAOS = "LA"
    LATVIA = "LV"
    LEBANON = "LB"
    LESOTHO = "LS"
    LIBERIA = "LR"
    LIBYA = "LY"
    LIECHTENSTEIN = "LI"
    LITHUANIA = "LT"
    LUXEMBOURG = "LU"
    MADAGASCAR = "MG"
    MALAWI = "MW"
    MALAYSIA = "MY"
    MALDIVES = "MV"
    MALI = "ML"
    MALTA = "MT"
    MARSHALL_ISLANDS = "MH"
    MAURITANIA = "MR"
    MAURITIUS = "MU"
    MEXICO = "MX"
    MICRONESIA = "FM"
    MOLDOVA = "MD"
    MONACO = "MC"
    MONGOLIA = "MN"
    MONTENEGRO = "ME"
    MOROCCO = "MA"
    MOZAMBIQUE = "MZ"
    MYANMAR = "MM"
    NAMIBIA = "NA"
    NAURU = "NR"
    NEPAL = "NP"
    NETHERLANDS = "NL"
    NEW_ZEALAND = "NZ"
    NICARAGUA = "NI"
    NIGER = "NE"
    NIGERIA = "NG"
    NORTH_MACEDONIA = "MK"
    NORWAY = "NO"
    OMAN = "OM"
    PAKISTAN = "PK"
    PALAU = "PW"
    PALESTINE = "PS"
    PANAMA = "PA"
    PAPUA_NEW_GUINEA = "PG"
    PARAGUAY = "PY"
    PERU = "PE"
    PHILIPPINES = "PH"
    POLAND = "PL"
    PORTUGAL = "PT"
    QATAR = "QA"
    ROMANIA = "RO"
    RUSSIA = "RU"
    RWANDA = "RW"
    SAINT_KITTS_AND_NEVIS = "KN"
    SAINT_LUCIA = "LC"
    SAINT_VINCENT_AND_GRENADINES = "VC"
    SAMOA = "WS"
    SAN_MARINO = "SM"
    SAO_TOME_AND_PRINCIPE = "ST"
    SAUDI_ARABIA = "SA"
    SENEGAL = "SN"
    SERBIA = "RS"
    SEYCHELLES = "SC"
    SIERRA_LEONE = "SL"
    SINGAPORE = "SG"
    SLOVAKIA = "SK"
    SLOVENIA = "SI"
    SOLOMON_ISLANDS = "SB"
    SOMALIA = "SO"
    SOUTH_AFRICA = "ZA"
    SOUTH_SUDAN = "SS"
    SPAIN = "ES"
    SRI_LANKA = "LK"
    SUDAN = "SD"
    SURINAME = "SR"
    SWEDEN = "SE"
    SWITZERLAND = "CH"
    SYRIA = "SY"
    TAIWAN = "TW"
    TAJIKISTAN = "TJ"
    TANZANIA = "TZ"
    THAILAND = "TH"
    TIMOR_LESTE = "TL"
    TOGO = "TG"
    TONGA = "TO"
    TRINIDAD_AND_TOBAGO = "TT"
    TUNISIA = "TN"
    TURKEY = "TR"
    TURKMENISTAN = "TM"
    TUVALU = "TV"
    UGANDA = "UG"
    UKRAINE = "UA"
    UNITED_ARAB_EMIRATES = "AE"
    UNITED_KINGDOM = "GB"
    UNITED_STATES = "US"
    URUGUAY = "UY"
    UZBEKISTAN = "UZ"
    VANUATU = "VU"
    VATICAN_CITY = "VA"
    VENEZUELA = "VE"
    VIETNAM = "VN"
    YEMEN = "YE"
    ZAMBIA = "ZM"
    ZIMBABWE = "ZW"

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
        with open("app\\database\\table_names.json", 'r') as file:
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
    admin_id: int | None = Field(default=None, foreign_key="adminuser.id", primary_key=True, index=True)
    permission_id: int | None = Field(default=None, foreign_key="permission.id", primary_key=True, index=True)


class BaseMatch(SQLModel):
    """Base match model\n
    begin: datetime
    end: datetime
    part: int
    """
    begin: datetime
    end: datetime
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
    de_end_time: datetime | None = Field(default=None, description="the time a player cast their domain")
    bv_end_time: datetime | None = Field(default=None, description="the time a player cast their binding_vow")
    sd_end_time: datetime | None = Field(default=None, description="the time a player cast their simple_domain")


class BaseVote(SQLModel):
    '''
    ### The base class for a vote
    `player_id: int = Field(foreign_key="player.id", ondelete="RESTRICT")`
    `ct_app_id: int = Field(foreign_key="ctapp.id", ondelete="RESTRICT")`
    '''
    player_id: int | None = Field(default=None, foreign_key="player.id", ondelete="RESTRICT", index=True)
    ct_app_id: int | None = Field(default=None, foreign_key="ctapp.id", ondelete="RESTRICT", index=True)