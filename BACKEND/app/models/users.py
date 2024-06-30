#./api/models/users.py
'''the module for handling the users models'''
from sqlmodel import Field, SQLModel
from pydantic import EmailStr
from datetime import date

# create your models here

class BaseUser(SQLModel):
	'class that represents a base user'
	email: EmailStr = Field(description='The email of a user.', unique=True, index=True)
	username: str = Field(description='The username of the user.',
					   max_length=30, unique=True, index=True)
	country: str | None = Field(default=None, description='The country of residence of the user.')

class User(BaseUser, table=True):
	'class that represents an User stored in the Database. It is a subclass of BaseUser'
	id : int | None = Field(default=None, primary_key=True)
	password: str = Field(description='The hashed password of the user')
	created: date | None = Field(default=None)

class CreateUser(BaseUser):
	'a class for creating a user. It is a subclass of BaseUser'
	password: str = Field(description='The password of the user',
					   min_length=8)
	confirm_password: str = Field(description='The password of the user, re-entered.',
							   min_length=8)
	model_config = {
		"json_schema_extra": {
			"examples": [
				{
					"email": "user@example.com",
					"username": "uniqueUsername",
					"country": "yourResidence",
					"password": "Anothersecret>8",
					"confirm_password": "Anothersecret>8",
				},
			]
		}
	}

class UserInfo(SQLModel):
	'class representing the user info sent to the client-side'
	id : int
	created: date
	email: EmailStr = Field(description='The email of a user.')
	username: str = Field(description='The username of the user.')
	country: str | None = Field(title='The country of residence of the user.')

class UserUpdate(SQLModel):
	'class for updating user info, except password'
	username: str | None = Field(description='The username of the user.')
	email: EmailStr | None = Field(description='The email of a user.')
	country: str | None = Field(title='The country of residence of the user.')

