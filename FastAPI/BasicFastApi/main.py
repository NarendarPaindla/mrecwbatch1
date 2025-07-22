from fastapi import FastAPI
from fastapi.params import Body
app=FastAPI()
posts=[]
@app.get("/")
def root():
    return {"message":f"{posts}"}

@app.post("/createpost")
def create_post(hexa: dict= Body(...)):
    posts.append(hexa)
    return {f"post created, {hexa['title']},{hexa['content']}"}

