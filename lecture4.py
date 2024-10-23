# REQUEST BODY -- LECTURE 4

from fastapi import FastAPI
from pydantic import BaseModel
# from typing import Optional

app = FastAPI()

class Item(BaseModel):
    #pass
    name: str
    description: str | None = None    # we want to make description optional, if we using python 3.6 to 3.10, we will use optional from 'typing' module
    # description: Optional[str] = None  (bydefault none value)
    price: float
    tax: float | None = None          # we can skip '= None'


@app.post("/items")
async def create_item(item: Item):
    return item

# a json wil be invalid if there is a trailing comma(,) after the last element

'''
now, if we want to specify what kind of output should a function return, we can do that also:
async def create_item(item: Item) -> Item:    or 
async def create_item(item: Item) -> str:
'''

@app.post("/items")
async def create_item(item: Item):
#    item_dict = item.dict()     # this is a built-in method with pydantic, now deprecated
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict     # we are returning a dictionary


'''
since item was a class, we can use item.tax, if it was dictionary we will have to use:
item['tax'] or item.get('tax')
'''

@app.put("/items/{item_id}")
async def create_item_with_put(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}

# ** is a spread operator that unpacks the content of the dictionary


@app.put("/items/{item_id}")
async def create_item_with_put(item_id: int, item: Item, q: str | None = None):   # q is a query parameter
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result
