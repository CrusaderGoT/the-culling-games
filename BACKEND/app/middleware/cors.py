from fastapi.middleware.cors import CORSMiddleware
from api.settings import app


# MIDDLEWARE
origins = [
    "http://localhost:8000",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://the-culling-games.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)