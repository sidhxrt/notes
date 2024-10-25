# RESPONSE STATUS CODES -- LECTURE 15

'''
A generic FastAPI response without Response Status Codes will only display 200 and 422 as response types.
If, for example, you have a route that creates a new item (a POST) route 
or one that returns no data then you would want to change the status code to something like a 201 or 204 
so that it is more easily understood by consumers of your API.
'''

from fastapi import FastAPI, status

app = FastAPI()

@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}

@app.delete("/items/{pk}", status_code=status.HTTP_204_NO_CONTENT)   # instead of directly mentioning the status code, we can use status object of fastapi
async def delete_item(pk: str):
    print("pk", pk)
    return pk      # we can simply write 'return', it wont create any difference as 'pk' wont be returned anyways

@app.get("/items/", status_code=status.HTTP_302_FOUND)
async def read_items_redirect():
    return {"hello": "world"}

# using status object of fastapi eliminates the need to remember what every status code does