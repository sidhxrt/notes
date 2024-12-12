# REQUEST FILES -- LECTURE 17

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse 

app = FastAPI()

@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}          # it can support .txt file but not .jpeg; if only 'len(file)' is asked and not 'file', it can support pdf files also
# try this here: return {"file": file}, it will not return bytecode or something, it will just return the contents of text file

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}  # it can support any filetype(check docs for more info)
# try this here: return {"file": file}, it will not return bytecode or something, it will return lot of information about the file in json format(dictionary)

# its better to use UploadFile than bytes-File as here fastapi knows ki a file is being uploaded and is not expecting a bytes object
'''
one more good thing about using UploadFile is that we can do the following stuffs too:
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    content = await file.read()
    return {"filename": file.filename}
'''
# READ ABOUT SPOOLED TEMPORARY FILE FROM STARLETTE DOCS(OR SEARCH IN STARLETTE-GITHUB)

# Now, lets make the upload option optional and not required; and can even send additional parameters/information like how we did in Body, Field, Query paramters
@app.post("/files/")
async def create_file(file: bytes | None = File(None, description="a file read as bytes")):
    if not file:
        return {"message": "No file sent"}
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile | None = None):
# async def create_upload_file(file: UploadFile = File(... , description="a file read as UploadFile")): 
    if not file:
        return {"message": "No upload file sent"}
    return {"filename": file.filename}


# now if we want to upload multiple files:
@app.post("/files/")
async def create_file(files: list[bytes] = File(..., description="a file read as bytes")):
    return {"file_size": [len(file) for file in files]}    # List comprehension is used here

@app.post("/uploadfiles/")
async def create_upload_file(files: list[UploadFile] = File(... , description="a file read as UploadFile")): 
    return {"filename": [file.filename for file in files]} # List comprehension is used here


# if we go to localhost:8000/, it will render this HTML:
@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
    """
    return HTMLResponse(content=content)
