from dotenv import load_dotenv
import os
from fastapi import HTTPException
import mysql
from mysql.connector import Error
load_dotenv()
DB_CONFIG={
    'host':os.getenv('DB_HOST'),
    'port':os.getenv('DB_PORT'),
    'user':os.getenv('DB_USER'),
    'password':os.getenv('DB_PASSWORD'),
    'database':os.getenv('DB_NAME'),
}
def get_db_connection():
    try:
        conn=mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        raise HTTPException(status_code=500,detail=f"DB connection Error: {e}")