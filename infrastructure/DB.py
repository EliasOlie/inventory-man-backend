from .Database import Database
import os

DB_URL = os.getenv('DB_HOST')

DB = Database(DB_URL)