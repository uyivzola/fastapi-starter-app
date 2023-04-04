# Importing necessary libraries, modules, and dependencies
from fastapi import FastAPI

from . import models
from .database import engine
from .routers import auth, posts, users, vote
# interacting with DATABASE
# copy + paste from fastapi website
# Creating database tables using metadata in models.py and the database engine.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()  # Creating a FastAPI instance called app

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

# Defining a GET route at the root (/) URL that returns a message.
@app.get('/')
def root():
    return {"message": "Hello World!!"}