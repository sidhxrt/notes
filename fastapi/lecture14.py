# EXTRA MODELS -- LECTURE 14

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
app = FastAPI()

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None
    
def fake_password_hasher(raw_password: str):
    return f"supersecret{raw_password}"

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
    # .dict() or .model_dump() is a pydantic method that converts model to dictionary
    # ** is used to unpack the content of dictionary into a string
    print("User 'saved'.")
    return user_in_db

@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

'''
if we do the following:
print(
    UserInDB(
        username="hello",
        email="hello@world.com"
        hashed_password="password"
        hello="world"
        random="randomword"
    )
)
it will print the following:
username='hello' hashed_password='password' email='hello@world.com' full_name=None
so even if we give hello, random it will not take it as they are not members of class
similarly, even if we send password(as we did in the fake_save_user()), UserInDB will just ignore it
'''


# now lets rewrite all the above code in a much optimized manner(with no repetition)
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
app = FastAPI()

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserIn(UserBase):   # UserIn will inherit from UserBase
    password: str

class UserOut(UserBase):
    pass

class UserInDB(UserBase):
    hashed_password: str
    
def fake_password_hasher(raw_password: str):
    return f"supersecret{raw_password}"

# rest of the code remains same



# NOW
from typing import Union

class BaseItem(BaseModel):
    description: str
    type: str

class CarItem(BaseItem):
    type = "car"

class PlaneItem(BaseItem):
    type = "plane"
    size: int

items = {
    "item1": {"description": "road", "type": "car"},
    "item2": {
        "description": "air",
        "type": "plane",
        "size": 5
    }
}

@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):  #instead of str we can also use Literal["item1", "item2"]
    return items[item_id]

# in python 3.10, we can use | instead of Union(we cant in the route-decorator, rest everywhere we can use it)
# Union[A, B] is the same as A | B


# NOW
class ListItem(BaseModel):
    name: str
    description: str

@app.get("/list_items/", response_model=list[ListItem]) # if we dont use response_model, the response body will be expecting just a string
async def read_items():
    return items

@app.get("/arbitrary", response_model=dict[str, float])  # key is string, value is float in dict[str, float]
async def get_arbitrary():
    return {"a": 1, "b":"2"}  # fastapi will convert string 2 to float 2
