from fastapi import FastAPI, HTTPException
from db.connection import get_db_connection
from routes.product import router as product_router
app=FastAPI()

app.include_router(product_router)
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
