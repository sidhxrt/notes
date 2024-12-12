# QUERY PARAMETERS & STRING VALIDATION -- LECTURE 5

# we are going to perform string validation on query parameters
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items")
async def read_items(q: str | None = Query(None, min_length= 3, max_length= 10)):
    results = {"items": [{"item_id": "aaa"}, {"item_id": "bbb"}]}
    if q:
        results.update({"q": q})
    return results

'''
to perform string validation on query parameters, we gonna use Query method from fastapi; we can check docs to know more about its functionalities.
so instead of writing 'q: str | None = None' we can write 'q: str | None = Query(None)' , its the same thing.
we can add additional parameters such as min_length and max_length which decides the min and max length of q.
'''

# we can add regular expressions as well
@app.get("/items")
async def read_items(q: str | None = Query(None, min_length= 3, max_length= 10, regex= "^fixedquery$")):   # regex expects presence of 'fixedquery' in the q, else it will throw error
    results = {"items": [{"item_id": "aaa"}, {"item_id": "bbb"}]}
    if q:
        results.update({"q": q})
    return results

# if we want to pass a default value which is not None/null, then we can do the following:
@app.get("/items")
async def read_items(q: str = Query("fixedquery", min_length= 3, max_length= 10)):  # here the default value is 'fixedquery' 
    results = {"items": [{"item_id": "aaa"}, {"item_id": "bbb"}]}
    if q:
        results.update({"q": q})
    return results

# if we pass in url/items, we will get q as 'fixedquery'
# if we pass in url/items?q=hi, then we will get q as 'hi'

'''
ellipsis(...) are used as placeholders in python.
they let us execute the program without crying, for example:
def functionn():
    ...

function()

it will work(it wont do anything, but wont show error either) :)
'''

# if we want to make a query parameter required and not optional:
@app.get("/items")
async def read_items(q: str ):  
    results = {"items": [{"item_id": "aaa"}, {"item_id": "bbb"}]}
    if q:
        results.update({"q": q})
    return results

# however, if we want to include some validation on query parameter(which is required and not optional), then we will have to use ellipsis.
@app.get("/items")
async def read_items(q: str =Query(..., min_length=3, max_length=10)):  
    results = {"items": [{"item_id": "aaa"}, {"item_id": "bbb"}]}
    if q:
        results.update({"q": q})
    return results
# we cannot write 'async def read_items(q: str =Query(, min_length=3, max_length=10)):' as it will throw error.


# if we want to add multiple values through url to query parameter:
# url.com/items?q=a&q=b&q=c&q=d
# this will take query parameter as q=d and ignore rest. to handle this, we will do the following:
@app.get("/items")
async def read_items(q: list[str] | None= Query(None)):  
    results = {"items": [{"item_id": "aaa"}, {"item_id": "bbb"}]}
    if q:
        results.update({"q": q})
    return results

# url.com/items?q=a&q=b&q=c&q=d
# query parameter will be "q": ["a", "b", "c", "d"] 

# if we want to set default value, we can write the following:
# async def read_items(q: list[str] =Query(["aaa", "bbb"])):  

# lets add metadata
# async def read_items(q: str | None =Query(None, min_length=3, max_length=10, title="this is title of q", description="this is description of q", deprecated=True)):  


# python is a snake-case language, so it wont be happy if we give query parameter name as 'item-id', but we do use that in url
# so to facilitate the use of - in name of query parameter, we use 'alias' parameter of Query method
@app.get("/items")
async def read_items(q: list[str] | None= Query(None, alias="item-number")):  
    results = {"items": [{"item_id": "aaa"}, {"item_id": "bbb"}]}
    if q:
        results.update({"q": q})
    return results

# now in url we shouldnt type url/items?q=value
# we should type url/items?item-number=value
# query parameter is read as item-number in url and not q anymore


# lets see how to hide something
@app.get("/items_hidden")
async def hidden_query_route(hidden_query: str | None= Query(None, include_in_schema=False)):  
    if hidden_query:
        return {"hidden_query": hidden_query}
    return {"hidden_query": "Not found"}

# if we execute url.com/items_hidden?hidden_query=aaa
# it will return {"hidden_query": aaa}

# if we execure url.com/items_hidden
# it will return {"hidden_query": "Not found"}

# in swagger docs, we wont find an option to input hidden_query, this makes it different from 'just' query parameter