# DEPENDENCIES INTRO -- LECTURE 22


# read about dependency injection
"""
dependencies are like middleware but they are not middleware, 
what they do is it takes functionality that we need to abstract out of a path operation 
and put it into the path operation.

now, this could have to do with security, 
it could have to do with um if there are multiple routes that have shared logic, 
it could have to do if we want to set up database connections 
and things like that.
"""

from fastapi import FastAPI, Depends

app = FastAPI()

@app.get("/items/")
async def read_items(q: str | None = None, skip: int = 0, limit: int = 100):  # we are passing in a query string(query parameter) and then we are passing in pagination parameters.
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/users/")
async def read_users(q: str | None = None, skip: int = 0, limit: int = 100):  
    return {"q": q, "skip": skip, "limit": limit}

# here we got lot of common(repeated) code, we can avoid the redundancy/repetition by using dependencies.
# we can see there are lot of common functionalities present in both the methods, we can write a method that serves those common functionalities and inherit from it.
# it is kind of like class inheritance, we got something similar to base class from we are inheriting, hence it is kind of a middleware 

async def common_parameters(q: str | None = None, skip: int = 0, limit: int= 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons

@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons

"""
we get the exact same functionality as we got before, 
but we were able to abstract the repeated code out of the 2 individual methods 
and create one common method that actually holds all this information
"""

# we can even nest the 'common_parameters' function:
async def hello():
    return "world"

async def common_parameters(
        q: str | None = None, skip: int = 0, limit: int = 100, blah: str = Depends(hello)
):
    return {"q": q, "skip": skip, "limit": limit, "hello": blah}

# we are able to do dependency injection with this hello method.