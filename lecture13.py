# RESPONSE MODEL -- LECTURE 13

# all that we are doing here(in this lecture) is for documentation purposes

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr   # we will have to install pydantic[email] to use EmailStr

app = FastAPI()

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

@app.post("/user/", response_model=UserIn)    # here instead of just returning string in the response, we are structuring how the response will look like
async def create_user(user: UserIn): 
    return user



# we wont be returning password in response lol, we need to make sure its protected
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserIn(UserBase):
    password: str

class UserOut(UserBase):   # if needed we can avoid this class and directly use UserBase
    pass

@app.post("/user/", response_model=UserOut)    
async def create_user(user: UserIn): 
    return user

# this will not return the password in response
'''
using response model is way time saving, we dont have to write the following kind of code to not return password:
for k, v in user.dict().items():
    if k != 'password':
'''



from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []

items = {
    "aaa": {"name": "Aaa", "price": 50.2},
    "bbb": {"name": "Bbb", "description": "the description", "price": 62, "tax": 20.2},
    "ccc": {"name": "Ccc", "description": None, "price": 50.2, "tax": 10.5, "tags": []}        
}

@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: Literal["aaa", "bbb", "ccc"]):   
    return items[item_id]

# response_model_exclude_unset=True will not include the default values or values(field values) which are not set explicitly in the response model.
# Literal types indicate that some expression has literally a specific value.
# in the above function, only expressions that have literally the value “aaa” or "bbb" or "ccc" will be accepted.


# we wanna write clean and non repeating code, so we will write model only once and use include and exclude statements to customize it according to our needs
@app.get("/items/{item_id}/name",
         response_model=Item,
         response_model_include={"name", "description"} # response_model_include(or exclude) expects a set and not list, but if we give list of values as input, fastapi automatically converts it to set
)
async def read_item_name(item_id: Literal["aaa", "bbb", "ccc"]):
    return items[item_id]


@app.get("/items/{item_id}/public",
         response_model=Item,
         response_model_exclude={"tax"}
)
async def read_item_public_data(item_id: Literal["aaa", "bbb", "ccc"]):
    return items[item_id]
