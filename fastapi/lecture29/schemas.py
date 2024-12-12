# 003 starts

from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    description: str | None = None

class ItemCreate(BaseModel):
    pass

class Item(ItemBase):
    id: int
    owner_id: int

    # lets also create a config class
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True

# check docs for pydantic config class (https://pydantic-docs.helpmanual.io/usage/model_config/)

"""
normal behavior of pydantic:
pydantic models expect data as dictionaries by default. 
if you try to pass an ORM object directly, it won't know how to convert it into a response.

Python dictionaries can only be accessed using the syntax A["key_a"]. 
The syntax A.key_a is not valid for dictionaries. 
The second syntax is used for objects (or instances of classes) where key_a is an attribute of the object.

Without orm_mode = True, if you pass an ORM object (e.g., a SQLAlchemy object) to a Pydantic model, 
Pydantic will not know how to access the ORM attributes (like user.items). 
It expects dictionary-like data, and attribute-style access (user.items) will fail because the model isn't configured to handle ORM objects.
"""

# 003 ends