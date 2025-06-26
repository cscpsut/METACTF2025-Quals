# db.py
import pymysql
from pymysql.constants import CLIENT

DB_HOST = '127.0.0.1'
DB_USER = 'appuser'
DB_PASS = 'REDACTED'
DB_NAME = 'traveliny'

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        autocommit=True,
        client_flag=CLIENT.MULTI_STATEMENTS,
        cursorclass=pymysql.cursors.Cursor
    )
