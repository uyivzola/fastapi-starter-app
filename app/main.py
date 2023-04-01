# Importing necessary libraries, modules, and dependencies
import time

import psycopg2 as psql
from fastapi import FastAPI

from . import models
from .database import engine
from .routers import posts, users, auth

# interacting with DATABASE
# copy + paste from fastapi website
# Creating database tables using metadata in models.py and the database engine.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()  # Creating a FastAPI instance called app

while True:
    try: #  Attempting to connect to a PostgreSQL database with the given credentials.
        conn = psql.connect(host='localhost', database='fastapi',
                            user='postgres', password='1234')
        cursor = conn.cursor()  # If the connection is successful, a cursor is created to execute SQL statements.
        print(" ✅ 🌚 DATABASE 🧠 📡 CONNECTED 🔗 ")
        break
    except Exception as error: # If there is an exception, the error is printed and the program sleeps for 2 seconds before trying to connect again.
        print('NO CONNECTION!❌🔗', error)
        time.sleep(2)


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

# Defining a GET route at the root (/) URL that returns a message.
@app.get('/')
def root():
    return {"message": "Hello World!!"}

