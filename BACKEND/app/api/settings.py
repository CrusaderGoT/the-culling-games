'''settings for the api'''
from fastapi import FastAPI
import os
from dotenv import load_dotenv

# load .env
load_dotenv()

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

# Time Constants for durations in Minutes
TIME_DUR = dict(MATCH_TIME=15, DOMAIN_TIME=5, SIMPLE_DOMAIN_TIME=5, BINDING_TIME=5, BINDING_LIMIT=3)
'A dictionary of the `times duration in Minutes` for specific events. e.g, MATCH_TIME'

TIME_AMT = dict(DOMAIN=5, SIMPLE_DOMAIN=5, BINDING=5)
'A dictionary of the amount of times an action can be done in a match. e.g, DOMAIN x5'

ACT_POINT = dict(VOTE_POINT=0.2, ACT_BINDING=5, ACT_DOMAIN=10, ACT_SIMPLE=7, DOMAIN_GAIN=4, SIMPLE_GAIN=2)
'A dictionary of the point needed/gained for/from specific actions. e.g, VOTE_POINT'

