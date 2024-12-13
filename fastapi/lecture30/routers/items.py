from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_token_header

router = APIRouter(
    prefix="/items", #so whenever we define routes later, we dont have to do "/items/{item_id}", we can directly type "/{item_id}"
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}}   
)

fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}

@router.get('/')  # this is actually /items/
async def read_items():
    return fake_items_db

@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}

@router.put("/{item_id}", tags=["custom"], responses={403: {"description": "operation forbidden"}}) # so whenever 403 occurs, this will come as description.
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(status_code=403, detail="you can only update the item: plumbus") # and this will also be displayed as the detail.
    return {"item_id": item_id, "name": "the great plumbus"}
