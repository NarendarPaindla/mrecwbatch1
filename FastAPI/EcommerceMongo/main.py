from fastapi import FastAPI, HTTPException
from db.connection import db
app=FastAPI()

@app.get("/ping")
def ping():
    record=db.ping_test.find_one({},{"_id":0,"message":1})
    if not record:
        raise HTTPException(status_code=404,detail="No ping record found")
    return {"message_from_db":record["message"]}