from application.exceptions import Exept
from decouple import config
import os
import psycopg2

if os.getenv("ENV"):
    ENV = os.getenv("ENV")
else:
    ENV = config("ENV")

class Database:
    
    def __init__(self, db_name, db_user, db_host, db_password) -> None:
        self.db_name = db_name
        self.db_user = db_user
        self.db_host = db_host
        self.db_password = db_password
        self.data_fetched = None
        if ENV == 'prod':
            self.conn = psycopg2.connect(database=self.db_name, user=self.db_user, host=self.db_host, password=self.db_password, sslmode='require')
        if ENV == 'dev':
            self.conn = psycopg2.connect(database=self.db_name, user=self.db_user, host=self.db_host, password=self.db_password)

    def insert(self, table, data):
        with self.conn:
            with self.conn.cursor() as cur:
                try:
                    cur.execute(f'INSERT INTO {table} VALUES({data})')
                    self.conn.commit()
                    return 0
                except Exception as e:
                    self.conn.rollback()
                    return {'Code':1, 'error':e}
    
    def create_user(self, table, data):
        with self.conn:
            with self.conn.cursor() as cur:
                try:
                    cur.execute(f"INSERT INTO {table} SELECT * FROM json_populate_record(NULL::{table}, '{data}')")
                    self.conn.commit()
                    return 0
                except Exception as e:
                    self.conn.rollback()
                    return {'Code':1, 'error':e}
        
    def read(self, table, identifier, fields='*', _json=False):
        with self.conn:
            with self.conn.cursor() as cur:
                
                cur.execute(f"SELECT {fields} FROM {table} WHERE {identifier}")
                self.conn.commit()
                self.data_fetched = cur.fetchall()

                if _json == True:
                    columns = list(cur.description)
                    results = []
                    for row in self.data_fetched:
                        row_dict = {}
                        for i, col in enumerate(columns):
                            row_dict[col.name] = row[i]
                        results.append(row_dict)
                    if len(results) <= 0:
                        return {"Code": 1, "error": "Not Found!"}
                    
                    return results
        
        if len(self.data_fetched) <= 0:
            return {"Code": 1, "error": "Not Found!"}
        
        return self.data_fetched
    
    def read_one(self, table, identifier=None, fields='*', _json=False):
        with self.conn:
            with self.conn.cursor() as cur:
                if identifier:
                    cur.execute(f"SELECT {fields} FROM {table} WHERE {identifier}")
                    self.data_fetched = cur.fetchall()
                    self.conn.commit()

                if _json == True:
                    user_obj = {}
                    for row in self.data_fetched:
                        colums = list(cur.description)
                        for i, col in enumerate(colums):
                            user_obj[col.name] = row[i]
                    if len(user_obj) <= 0:
                        raise Exept.UserNotFound("This user not found")

                    return user_obj
        
        return self.data_fetched

    def delete(self, table, identifier):
        with self.conn:
            with self.conn.cursor() as cur:
                try:
                    cur.execute(f'DELETE FROM {table} WHERE {identifier}')
                    self.conn.commit()
                    return 0
                except Exception as e:
                    return {"Code":1, "error": e}

    def update(self, table, field, value, identifier):
        with self.conn:
            with self.conn.cursor() as cur:
                try:
                    cur.execute(f"UPDATE {table} SET {field} = '{value}' WHERE {identifier}")
                    self.conn.commit()
                    return 0
                except Exception as e:
                    return {"Code":1, "error": e}
                    
    def __repr__(self) -> str:
        return f'{self.db_name}\n{self.db_user}\n{self.db_host}'

    def querie(self, q):
        with self.conn:
            with self.conn.cursor() as cur:
                try:
                    cur.execute(q)
                    self.conn.commit()
                    self.data_fetched = cur.fetchall()
                    return self.data_fetched
                except Exception as e:
                    return {"Code":1, "error": e}
    def rb(self):
        with self.conn:
            self.conn.rollback()
            print('Rolling back')

    def login(self, table, email):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(f"SELECT user_password FROM {table} WHERE user_email = '{email}'")
                self.data_fetched = cur.fetchone()
                self.conn.commit()
        return self.data_fetched