# DEPENDENCIES IN PATH OPERATION DECORATORS, GLOBAL DEPENDENCIES -- LECTURE 25


# till now we were using dependencies in path operation definition(methods basically), now we will be using them in path operation decorators

from fastapi import FastAPI, Depends, Header, HTTPException

app = FastAPI()

async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return "hello"

@app.get("/items")
async def read_items(blah: str = Depends(verify_token)):
    print(blah)
    return [{"item": "foo"}, {"item": "bar"}]

""" 
writing dependencies in path operation decorators is for when we need to check something, 
if we have functionality that we want returned to our path operation function, 
we cant put them in the decorator.

like if we wanted to actually use this key(verify_key or verify_token) somewhere in our function, 
then we cant put it in our decorator because we wont have access to it.
"""

# NOW
async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-key header invalid")

@app.get("/items", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():  # if we want to use the key in the function then we will have to write the Depends code in the function parameter like: async def read_items(key: str = Depends(verify_key))
    return [{"item": "foo"}, {"item": "bar"}]



# NOW LETS TALK ABOUT GLOBAL DEPENDENCIES
async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-key header invalid")

@app.get("/items", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items(): 
    return [{"item": "foo"}, {"item": "bar"}]

@app.get("/users", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_users(): 
    return [{"username": "sid"}, {"username": "yoo"}]

# now we can see that we have to write the dependencies code in every route decorator.
# we can get rid of this by using the concept of global dependencies

async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-key header invalid")

app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])

@app.get("/items")
async def read_items(): 
    return [{"item": "foo"}, {"item": "bar"}]

@app.get("/users")
async def read_users(): 
    return [{"username": "sid"}, {"username": "yoo"}]


# CONCLUSION:
# we put dependencies in our path operation decorator if we dont need the values that they return
# if we need to work with the values that are returned, we put them in the path operation function/ path operation definition