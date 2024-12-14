# STATIC FILES, TESTING AND DEBUGGING -- LECTURE 33


# STATIC FILES
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static", name="static"))
# this StaticFiles is separate from an API router, this is just going to separately mount it to the app

# if we hit localhost/static, we will not find anything(we will get {"detail": "Not Found"} in the webpage)
# if we hit localhost/static/index.html, we will be served the with the static file(index.html along with the styles)
# if we hit localhost/static/main.css, we will be served with the contents present in the main.css file 
"""
i.e (contents of main.css)
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    height: 100vh;
    display: grid;
    place-content: center;
}
"""

# now, lets look at TESTING, for that we will have to pip install pytest.
# we can write the testing code here, in the main file itself. but for good practice, we will create a separate 'test' directory

# TESTING
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI()

fake_secret_token = "coneofsilence"
fake_db = dict(
    foo = dict(
        id="foo", title="Foo", description="There goes my hero"
    ),
    bar=dict(
        id="bar", title="Bar", description="the bartenders"
    )
)

class Item(BaseModel):
    id: str
    title: str
    description: str | None = None

@app.get("/items/{item_id}", response_model=Item)
async def read_main(item_id: str, x_token: str = Header(...)):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]

"""
instead of:
if item_id not in fake_db:

we can write:
item = fake_db.get(item_id)
if item is None:
"""

@app.post("/items/", response_model=Item)
async def create_item(item: Item, x_token: str = Header(...)):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item.id in fake_db:
        raise HTTPException(status_code=400, detail="Item already exists")
    fake_db[item.id] = item
    return item
# we got our functionality here in the main file(lecture33.py), now we need to update the test file(test_main.py)
# head to test_main.py



# DEBUGGING

"""
debugging is IDE/editor spefic, we can go and edit configurations to set our own custom run configuration for a particular file/folder.
then we will have an option to 'debug' that runs the file according to the configurations set by us.
It behaves similar to the debug option(that we use before run option) in TurboC++
"""