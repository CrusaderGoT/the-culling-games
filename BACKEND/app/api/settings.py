"""settings for the api"""

import os

import socketio
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute

# load .env
load_dotenv()


def custom_generate_unique_id(route: APIRoute):
    return f"{route.name}"


app = FastAPI(
    title="The Culling Games API", generate_unique_id_function=custom_generate_unique_id
)
"""
The Global FastAPI app. To allow for use in multiple files.\n
* ### Everything needed for the initailization of the app instance, should be made in the same directory as where this app is instantiated. Eg. CORS, Middleware, etc.\n
#### example:
>>> from api.settings import app
>>> @app.get('/')
>>> # rest of your code
"""


# Create a Socket.IO server with asyncio
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=["http://localhost:3000"],
)
"""
The Global Socket.io server. To allow for use in multiple files.\n
Should typically be used by converting a router function
main code block to a `_sub_helper` function,
and then use that helper in both `sio`,`router`or`app`.
#### example:
>>> from api.settings import sio
>>> @sio.on("my_event")
>>> def my_event:
        _sub_helper()
"""

# Wrap the Socket.IO server with ASGIApp
ws_app = socketio.ASGIApp(sio)
"""The Websocket App, to be mounted on the main FastAI app."""

# Mount the Socket.IO app to a specific route
app.mount("/socket.io", ws_app)

# MIDDLEWARE
origins = [
    "http://localhost:3000",
    "https://the-culling-games.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# to get a string like this run:
# openssl rand -hex 32 in bash $
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
