# BIGGER APPLICATIONS - MULTIPLE FILES -- LECTURE 30

from fastapi import FastAPI, Depends

from .dependencies import get_token_header, get_query_token

"""
from .routers.users import router
from .routers.items import router # this will override the previous router(users ka)

app = FastAPI(dependencies=[Depends(get_query_token)])
app.include_router(router) # users router (wont work now)
app.include_router(router) # items router

to solve this issue there are couple of ways that we can do:
1. 
from .routers import users, items

app = FastAPI(dependencies=[Depends(get_query_token)])
app.include_router(users.router)
app.include_router(items.router)

2.
from .routers.users import router as user_router
from .routers.items import router as item_router

app = FastAPI(dependencies=[Depends(get_query_token)])
app.include_router(user_router)
app.include_router(item_router)

3. 
for this one, we will use the __init__.py under routers
and then make changes in main.py(in our case, lecture30.py) like how we did below.
"""

from .routers import users_router, items_router

app = FastAPI(dependencies=[Depends(get_query_token)])
app.include_router(users_router)
app.include_router(items_router)

@app.get("/")
async def hello():
    return "connection successful"
# for this route to work, we need to input the token(which is 'jessica')


# WE CAN INCLUDE APIROUTERS IN OTHER APIROUTERS, IT DOESNT HAVE TO JUST BE INTO THE MAIN APP.
# we can nest this sort of functionality and get creative about it.