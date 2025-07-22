from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
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
app=FastAPI()
def get_db_connection():
    try:
        conn=mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        raise HTTPException(status_code=500,detail=f"DB connection Error: {e}")
@app.get("/")
def root():
    return{"message":"Created basic structure successfully"}

@app.get("/ping")
def ping():
    conn=get_db_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT message FROM ping_test LIMIT 1;")
    result=cursor.fetchone()
    cursor.close()
    conn.close()
    if not result:
        raise HTTPException(status_code=404,detail="No ping record found")
    return {"message_from_db":result["message"]}
