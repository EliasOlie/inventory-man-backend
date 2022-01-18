from .Database import Database
import os

DB_NAME = os.getenv('name')
HOST = os.getenv('host')
USER = os.getenv('user')
PASSWORD = os.getenv('password')

DB = Database(DB_NAME, USER, HOST, PASSWORD)