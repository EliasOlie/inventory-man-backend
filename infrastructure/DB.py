from .Database import Database
from decouple import config
import os

if os.getenv("ENV"):
    ENV = os.getenv("ENV")
else:
    ENV = config("ENV")

if ENV == 'prod': 
    DB_NAME = os.getenv('name')
    HOST = os.getenv('host')
    USER = os.getenv('user')
    PASSWORD = os.getenv('password')
    DB = Database(DB_NAME, USER, HOST, PASSWORD)
    
if ENV == 'dev':
    DB = Database('man', 'postgres', "DB", 'admin')