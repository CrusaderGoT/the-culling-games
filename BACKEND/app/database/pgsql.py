'''a module that handles the connection of sqlmodel to postgresql\n
The engine object can be import from this module'''
import ssl
from sqlmodel import create_engine
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

SSL_CERT_PATH = os.getenv("SSL_CERT_PATH")
DATABASE_URL = os.getenv("DATABASE_URL")

# Create an SSL context
ssl_context = ssl.create_default_context(cafile=SSL_CERT_PATH)
ssl_context.verify_mode = ssl.CERT_REQUIRED

# create engine variable
engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"ssl": ssl_context}
    )