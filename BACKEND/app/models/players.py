from sqlmodel import Field, SQLModel
from enum import Enum


# create your models here




class BasePlayer(SQLModel):
    'A base Player class, for filtering data'
    class Gender(str, Enum):
        'the gender class for players'
        m = 'male'
        f = 'female'
        nb = 'non-binary'
    name: str = Field(description='The name of your Character.')
    role: str | None = Field(default='sorcerer',
                            description='The role of the player, i.e Occupation.')
    ethnicity: str | None = Field(default=None, description='The etnicity of the Player.')
    gender: Gender = Field(description='The gender of the Player.')
    age: int = Field(description='The age of the player', gt=0, le=102)

class Player(BasePlayer, table=True):
    'This class represents a complete player, as stored in the database'
    id : int | None = Field(default=None, primary_key=True,
                            title='Player ID', description='The id attribute of a Player Class')
    colony_id : int | None = Field(default=None, foreign_key='colony.id')
    user_id : int | None = Field(default=None, foreign_key='user.id')
    culled : bool = Field(default=False, description="The living status of a player; False = Alive, True = Dead")
    ct_id: str | None = Field(default=None, foreign_key="cursedtechnique.id", description="The Cursed Technique Id of the Player")

class CursedTechnique(SQLModel, table=True):
    'This class represents a cursed technique'
    id : int | None = Field(default=None, primary_key=True,
                            title='CT ID', description='The id attribute of a CT Class')
    name: str = Field(description='The name of the Cursed Technique')
    definition: str = Field(title='Cursed Technique',
                            description="The definition of the cursed technique, should not be a direct application.")
    applications: list[str] = Field(alias='cursed technique application', max_length=5, min_length=5,
                                    description='Explain an appliation of your Cursed Technique. Should not be able to beat Gojo Satoru')
    player_id: int | None = Field(default=None, foreign_key="player.id")
    
class Colony(SQLModel, table=True):
    'This class represents a colony'
    id : int | None = Field(default=None, primary_key=True, alias='number')
    location: str = Field(title='The name and location of the colony')
    image: bytes | None = Field(default=None)

class PlayerInfo(SQLModel):
    'The player info sent to the client-side'
    id : int
    name: str = Field(description='The name of your Character.')
    age: int = Field(description='The age of the player', gt=0, le=102)
    gender: str = Field(description='The gender of the Player.')
    role: str | None = Field(description='The role of the player, i.e Occupation.')
    ethnicity: str | None = Field(description='The etnicity of the Player.')
    cursed_technique: CursedTechnique = Field(description="Player's Cursed Technique")
    user_id : int = Field(description="Player's User Id")
    colony_id : int | None # will be promised/required later
    culled : bool = Field(description="The living status of a player; False = Alive, True = Dead")
    ct_id: int | None = Field(default=None, foreign_key="cursedtechnique.id", description="The Cursed Technique Id of the Player")
