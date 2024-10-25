# BODY - NESTED MODELS -- LECTURE 9

from fastapi import FastAPI, Body, Query, Path
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()

class Image(BaseModel):
    url: HttpUrl
    name: str

'''
we can do the following as well,
url: str = Field(
              ..., 
              regex='^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*)$'
              )

to avoid the messy code, we can go and check pydantic docs if they have some built-in validations for url,
we can use HttpUrl (3 dots on top-left of pydantic website > Usage >  Field Types > (ctrl f and search for url) URL > HttpUrl)
'''

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = []          # set[str] = set() also works, so if request's tags have multiple same values, the response will have only one value(like how set works)
    image: list[Image] | None = None

'''
if request body has: "tags": ["hello", "world", "hello"],
then response body has: "tags": ["hello", "world"]
'''

class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]            # we can use typing module as well, from typing import List; or we can simply type the expected data-type inside the [] for python 3.10

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

@app.post("/offers")
async def create_offer(offer: Offer = Body(..., embed=True)):
    return offer

@app.post("/images/multiple")
async def create_multiple_images(images: list[Image]):    # we can write this also: async def create_multiple_images(images: list[Image] = Body(..., embed= True)):
    return images

@app.post("/blah")
async def create_some_blahs(blahs: dict[int, float]):       # we can pass in dictionary of int-float like how we passed list 
    return blahs
# like how we can pass in arbitrary list, we can pass in arbitrary dictionary as well


# from typing import List
# we replace it with list[str]

# sexy website to get regex of urls/email/or any other entity
# ihateregex.io


# "unless we need something very custom, use the built-in stuff, it(built-in stuffs) is made for a reason"
