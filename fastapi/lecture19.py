# HANDLING ERRORS -- LECTURE 19

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel

app = FastAPI()

items = {"aaa": "this is item01"}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found", headers={"X-error":"there goes my error"})  # we can give custom headers as well with 'headers' parameter
    return {"item": items[item_id]}

'''
if we dont write the following code and then hit the url localhost8000/items/bbb then it will display 'internal server error'
if item_id not in items:
    raise HTTPException(status_code=404, detail="Item not found")
'''

# now lets extend the base-exception class, we cant (write same code again and again to)raise HttpException for every other thing

class UnicornException(Exception):    # we can give any name to this class
    def __init__(self, name):
        self.name = name

@app.exception_handler(UnicornException)  # we are throwing 'UnicornException' which is handled by our 'unicorn_exception_handler'
async def unicorn_exception_handler(request: Request, exc: UnicornException):  # exc is an instant of the class
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."}
    )

@app.get("/unicorns/{name}")
async def read_unicorns(name: str):
    if name == "yolo":
        raise UnicornException(name=name)  # we are instantiating the class with name='variable-name'
    return {"unicorn_name": name}

# we did all of this so that we dont have to write the HttpException code all the time to raise the exception in various path operations.
# now whenever we want to raise this exception, we can simply extend the exception class

# NOW
@app.exception_handler(RequestValidationError)  # we are throwing the RequestValdationError class 
async def validation_exception_handler(request, exc):  # we can give any name to this function
    return PlainTextResponse(str(exc), status_code=400)

@app.get("/validation_items/{item_id}")
async def read_validation_items(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="i dont like 3")
    return {"item_id": item_id}

'''
now in the browser,
if we hit 'localhost:8000/validation_items/5',
it will show '"item_id": 5'

if we hit 'localhost:8000/validation_items/3',
it will show '{"detail": "i dont like 3"}'

if we hit 'localhost:8000/validation_items/aa',
it will show:
1 validation error for Request
path -> item_id
    value is not a valid integer (type=type_error.integer)

but if we had commented line 47, 48, 49 and 
then if we hit 'localhost:8000/validation_items/aa',
it will show:
{"detail":[{"loc":["path", "item_id"],"msg":"value is not a valid integer","type":"type_error.integer"}]}
'''

# now lets add in another exception handler:
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

# NOW 
# lets extend the requestvalidationerror class
# its bydefault the class that shows 422 on swagger(when we get 422 error, we see a class that tells us about the error in the response body, that class it requestvalidationerror class)
# we are adding our parameters such as blahblah(which is the body here) to the requestvalidationerror class
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "blahblah": exc.body}) # blahblah is basically the body
    )

class Item(BaseModel):
    title: str
    size: int

@app.post("/items/")
async def create_item(item: Item):   # now if the request is not in the desired format, it will throw the above requestvalidationerror(including the blahblah parameter)
    return item


# sometimes we wanna send some parameters to client but rest everything default we want to send
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"omg! an http error: {repr(exc)}")   # repr means representation, repr(exc) means representation of the exception
    return await http_exception_handler(request, exc)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"omg! the client sent invalid data: {exc}")
    return await request_validation_exception_handler(request, exc)

@app.get("/blah_items/{item_id}")
async def read_items(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="i dont like 3")
    return {"item_id": item_id}

'''
so now if we hit localhost:8000/blah_items/3 on browser,
its gonna print the following on terminal:
omg! an http error: HTTPException(status_Code=418, detail="i dont like 3")

if we hit 'localhost:8000/validation_items/aa',
it will show:
omg! the client sent invalid data: 1 validation error for Request
path -> item_id
    value is not a valid integer (type=type_error.integer)

'''

# we have to use a PlainTextResponse to beautify the error that is shown to users on browser when they fuckup