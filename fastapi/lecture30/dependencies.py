from fastapi import Header, HTTPException

# async def get_token_header(x_token: str = Header(...)):   to avoid typing the x_token everytime in swagger, we will type the default value as 'fake-super-secret-token'
async def get_token_header(x_token: str = Header('fake-super-secret-token')):
    if x_token != 'fake-super-secret-token':
      raise HTTPException(status_code=400, detail="X-Token header invalid")

async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="no jessica token provided")
        