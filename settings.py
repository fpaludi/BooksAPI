import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

class Settings:
    DATABASE_URL = os.environ.get("DATABASE_URL")
    GOODREAD_API_KEY = os.environ.get("GOODREAD_API_KEY")
    GOODREAD_API_URL = os.environ.get("GOODREAD_API_URL")
    