# DECLARE REQUEST EXAMPLE DATA -- LECTURE 10

# we will be looking at 3 separate ways that we can include information about the request body
# 1st way is using a class config object
# so basically, the example request body(that we see in swagger docs), we can customize it

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    class Config:                     # this name should be Config
        json_schema_extra = {         # this name should be json_schema_extra
            "example": {
                "name": "sid",
                "description": "this is description",
                "price": 16.25,
                "tax": 1.67
            }
        }
    
    # class Config should be declared inside the model(class Item)


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results



# another way of doing this is by using the example parameter in the Field object, this is the 2nd way
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    name: str = Field(..., example= "sid")
    description: str | None = Field(None, example= "this is 2nd description")
    price: float = Field(..., example=2.22)
    tax: float | None = Field(None, example=1.2)

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results



# another way of doing this is by using the example parameter in the Body object, this is the 3rd way
from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str 
    description: str | None = None
    price: float 
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item = Body(
            ...,
            example={
                "name": "sid",
                "description": "this is the 3rd description",
                "price": 12.12,
                "tax": 2.5
            }   
        )
    ):
    results = {"item_id": item_id, "item": item}
    return results



# similar to example, we can also have examples
from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str 
    description: str | None = None
    price: float 
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item = Body(
            ...,
            examples={
                "normal": {                   #this may fuck up(description will not be shown in body, it will be shown differently), so we follow summary-description-value pattern as used below
                    "name": "sid",
                    "description": "this is normal description",
                    "price": 12.12,
                    "tax": 2.5
                },
                "converted": {
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert price 'strings' to 'integers' automatically",
                    "value": {
                        "name": "sid",
                        "price": "16.25"
                    }
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "description": "hello world",
                    "value": {
                        "name": "sid",
                        "price": "sixteen point two five"
                    }
                }
            }   
        )
    ):
    results = {"item_id": item_id, "item": item}
    return results

# when we use examples, we have to follow the following order(summary, description, value)