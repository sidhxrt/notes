# PATH PARAMETERS & NUMERIC VALIDATION -- LECTURE 6

# we are going to perform numeric validation on path parameters
# we will be using Path object(method) like how we used Query object for query parameters

from fastapi import FastAPI, Query, Path

app = FastAPI()

@app.get("/items_validation/{item_id}")
async def read_items_validation(
    item_id: int = Path(..., title="title of path parameter"), q: str | None = Query(None, alias="item-query") # ... is used as we dont usually set default value to path parameter
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# we dont usually have default parameter for path parameter


'''
we cant declare a non-default parameter after a default parameter in python
async def read_items_validation(
    item_id: int = Path(..., title="title of path parameter"), q: str 
):
this is not valid as we aint using "'=' and setting value to parameter q".
even though we are not assigning default parameter to item_id, but we are using '=', so python thinks it is assigned with some default parameter.
we can solve this by declaring 'q' before 'item_id' inside the arguments.
i.e:
async def read_items_validation(
    q: str, item_id: int = Path(..., title="title of path parameter") 
):
this is valid.
OR
we can use asterisk as the first argument(*)
'''

@app.get("/items_validation/{item_id}")
async def read_items_validation(
    *,
    item_id: int = Path(..., title="title of path parameter", gt=10, le=100),  # gt stands for greater than, ge for >=, le for <=, lt for < 
    q: str  
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# what * will do is, it will tell python ki all of the arguments after * are keyword arguments or kwargs
# args stands for arguments that are passed to the function whereas kwargs stands for keyword arguments which are passed along with the values into the function.


# we can do numeric validation for query parameters as well
@app.get("/items_validation/{item_id}")
async def read_items_validation(
    *,
    item_id: int = Path(..., title="title of path parameter", gt=10, le=100),  # gt stands for greater than, ge for >=, le for <=, lt for < 
    q: str,
    size: float = Query(..., gt=0, lt=7.75)  
):
    results = {"item_id": item_id, "size": size}
    if q:
        results.update({"q": q})
    return results
