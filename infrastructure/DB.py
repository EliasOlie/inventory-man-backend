from .Database import Database
from decouple import config
import os

DB_URL = os.environ(['DB_HOST'])

DB = Database(DB_URL)