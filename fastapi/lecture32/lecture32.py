# METADATA AND DOCS URLS -- LECTURE 32

from fastapi import FastAPI

description = """
MyApp API helps you do awesome stuff.

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""
# we are using doc strings for description, it will be rendered as markdown(hence we are using **, _, # and all)


tags_metadata = [
    dict(
        name="users",
        description="Operations with users. The **login** logic is also here."
    ),
    dict(
        name="items",
        description="Manage items. So _fancy_ they have their own docs.",
        externalDocs=dict(
            description="Items external docs", url="https://www.hornokplease.studio"
        )
    )
]

app = FastAPI(
    title="MyAPP",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact=dict(    # we can directly write a dictionary for contact instead of using dict, both the options are valid.
        name="Deadpoolio the Amazing",
        url="http://someurl.com/contactme",
        email="sample@email.com" 
    ),
    license_info=dict(
        name="Apache 2.0", url="https://www.apache.org/licenses/LICENSE-2.0.html"
    ),
    openapi_tags=tags_metadata,
    openapi_url="/api/v1/openapi.json", # now, when we hit 'localhost:8000/api/v1/openapi.json', we will get info about the apis.
    docs_url="/newdocs",  # now whatever we were getting at 'localhost:8000/docs', we will get it at 'localhost:8000/newdocs'.
    redoc_url=None   # we wont get the stuff that we were getting at /redoc at any api endpoint(not even /redoc)
)

@app.get("/users", tags=["users"])
async def get_users():
    return [dict(name="harry"), dict(name="Ron")]

@app.get("/items", tags=["items"])
async def read_items():
    return [dict(name="wand"), dict(name="flying broom")]