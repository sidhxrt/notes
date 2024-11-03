# REQUEST FORMS AND FILES -- LECTURE 18

# even if we use form and body together, fastapi will convert body into file
# similarly, if we use file, form, and body together, fastapi will again convert all it into file(multipart form-data)

from fastapi import FastAPI, File, UploadFile, Form, Body

app = FastAPI()

@app.post("/files/")
async def create_file(
    file: bytes = File(...),
    fileb: UploadFile = File(...),
    token: str = Form(...),
    hello: str = Body(...)
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
        "hello": hello
    }