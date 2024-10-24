# BODY - MULTIPLE PARAMETERS -- LECTURE 7

from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel

# like Query and Path, we have Body object(method) as well

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class User(BaseModel):
    username: str
    fullname: str | None = None

@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(..., title= "this is title of item_id", ge=10, le=150),
    q: str | None = Query(None),
    item: Item | None,
    user: User,
    importance: int = Body(...)
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    if user:
        results.update({"user": user})
    if importance:
        results.update({"importance": importance})
    return results

# if we declare 'importance: int' in the argument of update_item function, it will be treated as query parameter. 
# if we want to make importance as a request body parameter, we can create a pydantic-basemodel-class, but its too much work for one int variable
# so we can use Body() object

'''
now, if we want a key-value pair in the body with the key being item, we can do the following:
item: Item = Body(..., embed=True) in the function argument, the request body will then have a following structure:
{
    "item": {
        "name": "string",
        "description: "string",
        "price": 0,
        "tax": 0
    }
}
and not:
{
    "name": "string",
    "description": "string",
    "price": 0,
    "tax": 0
}
'''
