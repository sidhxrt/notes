# QUERY PARAMETERS -- LECTURE 3

# query parameters are just any sort of extra little tags that we want to put it at the end of url
# they allow for more dynamic searching 
# url.com/items?limit=1
# url.com/items?skip=2
# url.com/items?skip=2&limit=1


from fastapi import FastAPI

app = FastAPI()

fake_items_db = [{"item_name": "aaa"}, {"item_name": "bbb"}, {"item_name": "ccc"}, {"item_name": "ddd"}, {"item_name": "eee"}]

# path parameter is declared at both route and function, query parameter is declared at only function and not route
# query parameter is an item that is included in the function parameter
@app.get("/items")
async def list_items(skip: int=0, limit: int=10):
    return fake_items_db[skip : skip + limit]      #return fake_items_db ka elements from index position 'skip' to 'skip + limit'


# if we want to have both path and query parameters
# we first import 'optional' from 'typing'; we can skip this step if we using python 3.10 by using '|'

@app.get("/items/{item_id}")
async def get_item(item_id: str, q: str | None = None):    # 'q:str' alone wont work, 'q: str | None' will work
    if q:                      # if q is not null
        return {"item_id": item_id, "q": q}
    
    return {"item_id": item_id}

# if we were to use typing module
'''
from typing import Optional
...
async def get_item(item_id: str, q: Optional[str] = None):
'''

# lets see type conversion a bit now
# short: bool = False   short will be a boolean and by default its going to be False

@app.get("/items/{item_id}")
async def get_item(item_id: str, q: str | None = None, short: bool = False):    # 'q:str' alone wont work, 'q: str | None' will work
    item = {"item_id": item_id}
    if q:                      
        item.update({"q": q})

    if not short:
        item.update(
            {
                "description": "your mom"
            }
        )

    return item

# now here, we can play in the url
# url.com/items/hello?q=world&short=0   or   url.com/items/hello?q=world&short=False   or 'false' or 'no' or 'off'
# output will be:
# {"item_id":"hello", "q": "world", "description": "your mom"}
# url.com/items/hello?q=world&short=1   or   url.com/items/hello?q=world&short=True    or 'true' or 'yes' or 'on'
# output will be:
# {"item_id":"hello", "q": "world"}

# this use of on/yes/true is possible coz of type conversion by pydantic
# in python, if we declare default parameter then we cannot have non-default parameters after default parameters in the function declaration

# lets have multiple path parameters in one route
@app.get("/users/{user_id}/items/{item_id}")
async def get_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {
                "description": "your mom"
            }
        )
    
    return item

# if we wanna have required query parameters, then:
@app.get("/items/{item_id}")
async def get_item(item_id: str, sample_query_parameter: str, q: str | None = None, short: bool = False):    # 'q:str' alone wont work, 'q: str | None' will work
    item = {"item_id": item_id, "sample_query_parameter": sample_query_parameter}
    if q:                      
        item.update({"q": q})

    if not short:
        item.update(
            {
                "description": "your mom"
            }
        )

    return item

# here, sample_query_parameter is required query parameter