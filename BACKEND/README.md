
# The Culling Games
*This is a repository for the Implementation of the culling games from reddit, r/thecullinggames as a website/api.*
*Engineered using FastAPI and NextJS.*

## Basics
* The repo is divided into two directories (`BACKEND` and `FRONTEND`). The `BACKEND` holds the main logistics on how the 
games API are defined. Which includes the Database, Models, Routers, Middleware, and Authentication. While the `FRONTEND`
holds the design, user interface and experience of the games.

* It uses data validation via pydantic, fastapi, and python, with typescript on nextjs to make sure data is transfered, interpreted, and enforced.

* Database: Postgresql, with alembic for migration, etc... SQLModel/SQLAlchemy is used for communicating with the database in python.

## Running Locally
* You need python, vscode, and node installed. Fork this repository.\n
In the `BACKEND` directory in vscode, run `pip install -r requirements.txt`
**Finally**
- Backend: `uvicorn app.api.main:app --reload`
- FRONTEND: ` npm run dev`