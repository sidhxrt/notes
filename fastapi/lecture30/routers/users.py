from fastapi import APIRouter

router = APIRouter()

# the tags functionality here is really just for organization in the API
@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "rick"}, {"username": "morty"}]

@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "currentuser"}

@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}