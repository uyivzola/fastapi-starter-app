# all code are copied from sqlalchemy except SQLALCHEMY_DATABASE_URL credentials. You should write your db passwords somewhere
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
# import time

# import psycopg2

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_port}/{settings.database_name}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try: #  Attempting to connect to a PostgreSQL database with the given credentials.
#         conn = psycopg2.connect(host='localhost', database='fastapi',
#                             user='postgres', password='1234')
#         cursor = conn.cursor()  # If the connection is successful, a cursor is created to execute SQL statements.
#         print(" ✅ 🌚 DATABASE 🧠 📡 CONNECTED 🔗 ")
#         break
#     except Exception as error: # If there is an exception, the error is printed and the program sleeps for 2 seconds before trying to connect again.
#         print('NO CONNECTION!❌🔗', error)
#         time.sleep(2)
