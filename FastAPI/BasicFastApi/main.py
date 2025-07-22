from fastapi import FastAPI
from fastapi.params import Body
app=FastAPI()

@app.get("/")
def root():
    return {"message":"hello world"}

@app.post("/createpost")
def create_post(hexa: dict= Body(...)):
    return {f"post created, {hexa['title']},{hexa['content']}"}

