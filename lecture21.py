# JSON COMPATIBLE ENCODER AND BODY UPDATES -- LECTURE 21


from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

fake_db = {}

class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None

@app.put("/items/{id}")
async def update_item(id: str, item: Item):
    fake_db[id] = item
    print(fake_db)
    return "success"

# sometimes we may have a datatype that is not compatible with our database, so we will have to convert each individual field.
# so instead of manually going and do it, what we can do is we can use jsonable_encoder().
@app.put("/items/{id}")
async def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data
    print(fake_db)
    return "success"


# NOW
class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "the bartenders", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": None,
        "price": 50.2,
        "tax": 10.5,
        "tags": []
    }
}

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):   # we can use enum also here instead of str, so that the input is only "foo", "bar" or "baz"
    return items.get(item_id)

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded

"""
now if we hit the put request with the following body:
item_id: bar

{
"name": "Barz,
"description": null,
"price" 3
}

it will return the following in the response body:
{
    "name": "Barz",
    "description": null,
    "price": 3,
    "tax": 10.5,    # for item_id = bar, it will not show tax as 20.2, it will show the default value from the pydantic class item().
    "tags": []
}

when we hit put request with item_id that already exists in db, it will rewrite all the parameters associated with item_id in the db.
if some parameters are not included in the put request, it will not consider the already existing values of those parameters as current value.
instead, it will consider the default values which we have already declared in the pydantic type class as the current value of those parameters.
"""

# NOW
"""
The PATCH method in HTTP is used to make partial changes to an existing resource.
The PATCH method is similar to the PUT method, but PATCH is used to modify only part of a resource, 
while PUT replaces the entire resource.
"""
@app.patch("/items/{item_id}", response_model=Item)
def patch_item(item_id: str, item: Item):
    stored_item_data = items.get(item_id)
    if stored_item_data is not None:
        stored_item_model = Item(**stored_item_data)
    else:
        stored_item_model = Item()
    # now we will create the 'update_data' dictionary
    update_data = item.model_dump(exclude_unset=True)    # dict has been deprecated, it is now model_dump
    # exclude_unset=True will look to see what is not being passed in(which parameters are not passed in)
    updated_item = stored_item_model.model_copy(update=update_data)   # copy has been deprecated, it is now model_copy
    item[item_id] = jsonable_encoder(update_item)
    print(items[item_id])
    return updated_item

# PATCH request can be combined into PUT request as well by manually coding using 'exclude_unset=True'