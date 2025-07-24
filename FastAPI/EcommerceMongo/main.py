from fastapi import FastAPI, HTTPException
from db.connection import db
from routes.product import router as product_router
from routes.category import router as category_router
app=FastAPI()
app.include_router(product_router)
app.include_router(category_router)
@app.get("/ping")
def ping():
    record=db.ping_test.find_one({},{"_id":0,"message":1})
    if not record:
        raise HTTPException(status_code=404,detail="No ping record found")
    return {"message_from_db":record["message"]}