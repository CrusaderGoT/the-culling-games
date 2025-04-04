# This repo is Archived and no longer improved. Check out the new one I am working on at [The Culling Game](https://github.com/CrusaderGoT/The-Culling-Game)

# The Culling Games
*This is a repository for the Implementation of the culling games from reddit, r/thecullinggames as a website/api.*
*Engineered using FastAPI and NextJS.*

## Basics
* The repo is divided into two directories (`BACKEND` and `FRONTEND`). The `BACKEND` holds the main logistics on how the 
games API are defined. Which includes the Database, Models, Routers, Middleware, and Authentication. While the `FRONTEND`
holds the design, interaction with the backend, user interface, and user experience of the games.

* It uses data validation via pydantic, fastapi, and python, with typescript on nextjs to make sure data transfered is interpreted, and enforced correctly.

* Database: Postgresql, with alembic for migration, etc... SQLModel/SQLAlchemy is used for communicating with the database in python.

## THE CULLING GAMES
### __The User__
To particate in the games, you need to create a user. The user is capable of creating a player, casting a vote, etc.

### __The Player__
The player is the fighter in the games, one must be a user before making a player.

#### Cursed Technique
This is the ability of the player, and contains one to five applications, that will be voted on.
#### Barrier Technique
This are the advanced techniques of a player, i.e, domain expansion, simple domain, and binding vow. These gives different buffs to votes, i.e vote could x2 in points. Only players of grade 2 and up can use them.
#### Points
This is the players total points, gained through voting and winning matches, and is used to activate advanced techniques, or upgrade player.

### __Colony__
This is where players fight, each player belongs to a colony containing ten players in total, and they all fight fellow players from the same colony. A colony is situated in a country, i.e apart from colony number, a colony is refered to by the country it is situated in. Though matches will take place in different places in the colony.


## Running Locally
* You need python, vscode, and node installed.
* Fork this repository.\n
In the `BACKEND` directory in vscode, run `pip install -r requirements.txt`.
* And in the `FRONTEND` run `npm install`

**Finally**
- Backend: `uvicorn app.api.main:app --reload`
- FRONTEND: `pnpm run dev`

## Contribution
* If you have uderstanding of NextJS, FastAPI, SQLAlchemy/SQLModel, or Pydantic. It will be highly appreciated if you can contribute in the completion of this project.

### Work Needed
- **Frontend**: The frontend needs a lot of work. i have been focused on the backend, as that is my niche, but i am learning nextjs in order to complete the frontend (i already had sufficient knowledge on frontend technologies like JS, HTML, CSS). I am looking to do more work on it, especially at the dashboard, also i suck at design, so even contributing design, will be appreciated.

- **Backend**: The backend i would say is around 60-70% done, the major thing i am yet to do is api for generating location/image for a match. Also i need to add more routes for admins, match, etc. Scale up the middleware, and refactoring.

- **Documentaion**: This will be documenting the intricates of the app on the  README, helping to correct grammar, or even improving code documentation.

This doesn't cover everything needed to be done, it is the core things i can think of for now.
So if you have any contribution, mostly programming , and design skills, do reach out to me on github or reddit.

# **Repost on any relevant Jujutsu Kaisen group, that could get us progress. Thanks.**
