from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def root():
    return {"message":"hello world"}
@app.get("/about")
def about():
    return {"message":"This is about page"}
@app.get("/contact")
def contact():
    return {"message":"This is contact page"}