# FORM FIELDS -- LECTURE 16

# the request that we are passing need not be application/json, it can be something like x-www-form-urlencoded or multipart/form-data
# we have to install 'python-multipart' as well
from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()

# we are sending form-data through POST request
@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):  # username and password will be of the form 'application/x-www-form-urlencoded' and not 'application/json'
    print("password", password)
    return {"username": username}

# we are sending request-payload(json) through POST request
class User(BaseModel):
    username: str
    password: str

@app.post("/login-json/")
async def login_json(user: User): # we can write this as 'async def login_json(username: str = Body(...), password: str = Body(...)):'
    return user

# async def login(username: str = Form(...), password: str = Body(...)):
# if we do this, still it will be treated as form-data(json-body will be overriden by form)

'''
usually, if a form data is being sent from frontend, we use the x-www-form-urlencoded to send the data
if we have to send it as json from frontend then we will have to first manually set up the json object
then stringify it using fetch or axios; and then we will be using application/json in the backend 
'''