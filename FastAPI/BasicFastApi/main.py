from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
app=FastAPI()
posts=[]

class Post(BaseModel):
    title:str
    content:str
@app.get("/")
def root():
    return {"message":f"{posts}"}

@app.post("/createpost")
def create_post(post:Post):
    post_dict=post.dict()
    posts.append(post_dict)
    return {"message":post_dict}

