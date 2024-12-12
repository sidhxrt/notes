# PATH OPERATION CONFIGURATION -- LECTURE 20

from fastapi import FastAPI, status
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()   # tags is going to be a set of strings that we are initializing as empty set

@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED, tags=["items"])
async def create_item(item: Item):
    return item

@app.get("/items/", tags=["items"])
async def read_items(): 
    return [{"name": "aaa", "price": 42}]

@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "sid"}]

# the tags on the routes will organize the routes(i.e in the swagger ui, we can see that there will be 2 categories, items and users. under items, there will be post and get route and under users, there will just one get route)

# instead of writing it manually, we can use a class to assign tags-name; we can even assign multiple tags to a route(the route will appear again in that category)
class Tags(Enum):
    items = "items"
    users = "users"

@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED, tags=[Tags.items, Tags.users],
    summary="create an item",         # this will be displayed next to route in swaggerUI, by default it displays the function name under route
    #description="create an item with name, description"
    #"price, tax and"          
    #"a set of unique values"
    response_description="the created item"  # bydefault it will be "successful response" in the response section
)
async def create_item(item: Item):
    """
    instead of writing the description in the route ka description, we can use doc-strings.
    and write the decription here, inside the function.
    this description is rendered as markdown.
    now, here is the description to the function:

    create an item with all the information:

    - **name**: each item must have a name
    - *description*: a long description
    - _price_: required
    - __tax__: if the item doesnt have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    we usually write docstrings so that it can be viewed by users who will be using our APIs i.e for documentation purpose
    """
    return item

@app.get("/items/", tags=[Tags.items])
async def read_items(): 
    return [{"name": "aaa", "price": 42}]

@app.get("/users/", tags=[Tags.users])
async def read_users():
    return [{"username": "sid"}]

@app.get("/elements/", tags=[Tags.items], deprecated=True) # the concept of something that is deprecated is its no longer an active use, it is going to be removed in a future release
async def read_elements():
    return [{"item_id": "aaa"}]



"""
Python documentation strings (or docstrings) provide a convenient way of associating documentation with Python modules, functions, classes, and methods. 
It's specified in source code that is used, like a comment, to document a specific segment of code. 
Unlike conventional source code comments, the docstring should describe what the function does, not how.

Declaring Docstrings: 
The docstrings are declared using '''triple single quotes''' or triple double quotes just below the class, 
method, or function declaration. All functions should have a docstring.

Accessing Docstrings: 
The docstrings can be accessed using the __doc__ method of the object or using the help function. 

def my_function():
    '''Demonstrates triple double quotes
    docstrings and does nothing really.''' 
    return None

print("Using __doc__:")
print(my_function.__doc__)

print("Using help:")
help(my_function)
"""

# MAJOR RELEASE VS MINOR RELEASE
"""
Major release:
Introduces new features or overhauls existing functionality. 
Major releases may require structural database changes.

Minor release:
Addresses bugs and enhances performance. 
Minor releases usually don't require database changes and are routine changes. 
"""