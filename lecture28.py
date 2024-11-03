# MIDDLEWARE & CROSS ORIGIN RESOURCE SHARING(CORS) -- LECTURE 28

from datetime import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class MyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers['X-Process-Time'] = str(process_time)
        return response
    
# in order to add our middleware to our app, we write the following:
app.add_middleware(MyMiddleware)
# now the custom middleware that we have created have been added to our app

@app.get("/blah")
async def blah():
    return {"hello": "world"}
# now when we hit this route and get the response, we can see that the 'X-Process-Time' has been added to the headers section of the response(Response Headers)

# middleware is all about adding functionality to each route, we can add it to individual routers or we can add it to our entire app


# now lets apply this(concept of middleware) to CORS(Cross Origin Resource Sharing)
# first, we will set up some origins:
origins = ["http://localhost:8000", "http://localhost:3000"]
# and then:
app.add_middleware(CORSMiddleware, allow_origins=origins)

# now we can run frontend(at port 3000) without getting cors error

# check docs of 'class CORSMiddleware' to know about more attributes and parameters of the class that we can play with.