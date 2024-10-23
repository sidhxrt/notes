# INTRODUCTION -- LECTURE 1

from fastapi import FastAPI

# we are instantiating our app(creating instance of FastAPI)
app = FastAPI()

# routes
@app.get("/", description="this is our first route, GET method", deprecated=True)
async def base_root():
    return {"message": "get hello world"}

@app.post("/")
async def post():
    return {"message": "post hello world"}

@app.put("/")
async def put():
    return {"message": "put hello world"}

# we can set the server to run on specific port using the following command:
# uvicorn main:app --port=5000
