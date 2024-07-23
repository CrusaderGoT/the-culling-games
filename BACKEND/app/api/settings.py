'''settings for the api'''
from fastapi import FastAPI


app = FastAPI(title='The Culling Games API')
'''The Global FastAPI app. To allow for use in multiple files.
#### example:
>>> from api.settings import app
>>> @app.get('/')
>>> # rest of your code'''

# to get a string like this run:
# openssl rand -hex 32 in bash $
SECRET_KEY = "7f820bef39dd81f92e9935b30f029a74af7b7d1c5d8c85c855d6b22d093d485c"
ALGORITHM = "HS256"