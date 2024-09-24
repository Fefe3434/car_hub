import os
from dotenv import load_dotenv


if os.getenv("FLASK_ENV") == "production":
    if not load_dotenv('.env.prod', override=True):
        raise FileNotFoundError('No .env.prod file found')
else:
    if not load_dotenv('.env.dev', override=True):
        raise FileNotFoundError('No .env.dev file found')


class Config:

    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_PORT = os.getenv("MYSQL_PORT")
    MYSQL_URL = os.getenv("MYSQL_URL")

SECRET_KEY= 'FEFE_3434'

