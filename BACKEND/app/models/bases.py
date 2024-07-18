'''module for creating base classes/data models for other models.
\nrules:\n
should not import any class or object directly from any other model module.\n
base classes defined here cannot have fields annotated with any models outside this module.\n
write attributes in class string definition, for easier understanding of their structure when imported to other files.\n
should be imported only in other model modules.\n
'''
from sqlmodel import SQLModel, Field
from enum import Enum
from datetime import date
from pydantic import EmailStr
from typing import Union

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
    country: Union["Country", None] = None

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
    Base model for player info, without cursed technique info and user info\n
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