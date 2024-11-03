# SUB-DEPENDENCIES -- LECTURE 24


from fastapi import FastAPI, Depends, Body

app = FastAPI()

def query_extractor(q: str | None = None):
    return q

def query_or_body_extractor(
        q: str = Depends(query_extractor), last_query: str | None = Body(None)   # we can play with it by replacing Body() parameter with Cookie() parameter or Path() parameter
):
    if not q:           # 'if not q' == 'if we dont have q'
        return last_query
    return q

@app.post("/item")
async def try_query(query_or_body: str = Depends(query_or_body_extractor)):
    return {"q_or_body": query_or_body}