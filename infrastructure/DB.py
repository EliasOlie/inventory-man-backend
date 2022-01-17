from .Database import Database
from decouple import config

DB = Database('man', 'postgres', 'db', 'admin')