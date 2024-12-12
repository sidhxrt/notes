# PATH PARAMETERS -- LECTURE 2

from fastapi import FastAPI
from enum import Enum

app = FastAPI()

@app.get("/items")
async def list_items():
    return {"message": "list items route"}

@app.get("/items/{item_id}")        #{item_id} is the path parameter & it can be of any data type
async def get_item(item_id):
    return {"item id": item_id}

# if we run the above code, and hit localhost/items/5, then we will get the output as:
# { "item id": "5"}
# here, 5 is treated as string. well to avoid this, pydantic support exists in fastapi

@app.get("/items/{item_id}")        
async def get_item(item_id: int):   #here only integer path parameter is accepted, if any other data type is fed as path parameter, it will throw error
    return {"item id": item_id}

# now the output will be, {"item id": 5}


# the order in which the routes are defined matters, fastapi executes the first matching route from top to bottom
# hence, we should put the specific endpoint first, before the dynamic endpoint
@app.get("/users/me")
async def get_current_user():
    return {"message": "this is the current user"}

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    return {"user_id": user_id}

# if we had reversed the above order, then even if we type /users/me , it will return 'me' as output


###
class FoodEnum(str, Enum):
    fruitss = "fruits"           # if we put 'fruitss = "f fruits"', then path parameter wont accept fruitss, it ll accept f fruits
    vegetabless = "vegetables"
    dairyy = "dairy"

@app.get("/foods/{food_name}")
async def get_food(food_name: FoodEnum):
    if food_name == FoodEnum.vegetabless:
        return {"food_name": food_name, "message": "you are healthy"}
    
    if food_name.value == "fruits":
        return {
            "food_name": food_name,
            "message": "eating fruits",
        }
    return {"food_name": food_name, "message": "dairy item it is"}

# We use enums for constants, i.e., when we want a variable to have only a specific set of values.