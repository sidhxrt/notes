# BODY - FIELD -- LECTURE 8

# fastapi is a baby of starlette(python asgi framework) and pydantic(type support)

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    name: str               # without Field(), we can only give generic information/validation about the fields present in the pydantic-basemodel-class; hence we use Field() object to give more information/validation
    description: str | None = Field(
        None, title="this is title of description of item", max_length=300
    )
    price: float = Field(..., gt=0, description="the price must be greater than zero")
    tax: float | None = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    return results


@app.put("/moreitems/{item_id}")
async def update_more_item(item_id: int, item: Item = Body(..., embed=False)):
    results = {"item_id": item_id, "item": item}
    return results

# Field() object(method) is not a FastAPI concept, it is a pydantic concept, it allows us to add metadata about the fields in the pydantic-basemodel-class
# similar to how Body(), Query(), Path() allowed us to add metadata about Request-Body, Query and Path parameters respectively