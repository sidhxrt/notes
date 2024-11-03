# EXTRA DATA TYPES -- LECTURE 11

# UUID - Universally Unique Identifier
# there are lot of other data types(other than int, str, float and other primitive datatypes) in pydantic, check their docs for more info
# if we dont get the data type that we need(from pydantic), we can use regex to do the required data validation

from fastapi import FastAPI, Body
from datetime import datetime, time, timedelta
from uuid import UUID

app = FastAPI()

@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_date: datetime | None = Body(None),
    end_date: datetime | None = Body(None),
    repeat_at: time | None = Body(None),
    process_after: timedelta | None = Body(None)
):
    start_process = start_date + process_after
    duration = end_date - start_process
    return {
        "item_id": item_id, 
        "start_date": start_date,
        "end_date": end_date,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration   
    }


'''
go to python-IDLE and write the following code to know more about UUID:

import uuid 
from uuid import uuid4
uuid()

'''