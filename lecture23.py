# CLASSES AS DEPENDENCIES -- LECTURE 23


from fastapi import FastAPI, Depends

app = FastAPI()

class Cat:
    def __init__(self, name: str):
        self.name = name

fluffy = Cat("mr fluffy")

# here, we have created an instance of Cat class with fluffy(fluffy is an object of the class)
# like above, we are gonna convert our common query parameters into a class

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int =100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):  # depends ke andar ka CommonQueryParams is basically instantiating an instance of that Class and kind of spreading these(q: str | None = None, skip: int = 0, limit: int =100) out
    # depends ke andar ka CommonQueryParams is taking the parameters that we are setting in our initialization in our constructor
    response = {}
    if commons.q: 
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response

"""
if q=q, skip=0, limit=2 then response body will be like:
{
    "items": [
        {
            "item_name": "Foo"
        },
        {
            "item_name": "Bar"
        }
    ]
}
"""

# we can even handle path parameters as well using the above technique:
class CommonQueryParams:
    def __init__(self, item_id: int, q: str | None = None, skip: int = 0, limit: int =100):
        self.q = q
        self.skip = skip
        self.limit = limit
        self.item_id = item_id

# and there is actually no need to tell the type annotation that commons is going to be a CommonQueryParams type
# we can even remove the first CommonQueryParams, fastAPI will still figure out(infact, presence of first CommonQueryParams is just a verbose)
# verbose: using or expressed in more words than are needed.
async def read_items(commons=Depends(CommonQueryParams)):
    print(commons.item_id)

# another way to remove the verbose is instead of doing the above method of removing the first CommonQueryParams, we can remove the second CommonQueryParams.
async def read_items(commons: CommonQueryParams = Depends()):  # this will do the exact same thing as above
    print(commons.item_id)