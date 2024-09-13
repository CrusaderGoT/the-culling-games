'''settings for the api'''
from fastapi import FastAPI
import os
from dotenv import load_dotenv

# load .env
load_dotenv()

global app
app = FastAPI(title='The Culling Games API')
'''The Global FastAPI app. To allow for use in multiple files.
#### example:
>>> from api.settings import app
>>> @app.get('/')
>>> # rest of your code'''

# to get a string like this run:
# openssl rand -hex 32 in bash $
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")