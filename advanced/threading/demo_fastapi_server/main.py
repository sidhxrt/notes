from fastapi import FastAPI

app = FastAPI()

@app.get('/items/{item_id}')
async def read(item_id: int):
    return {'item_id': item_id}