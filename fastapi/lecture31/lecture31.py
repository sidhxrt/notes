# BACKGROUND TASKS -- LECTURE 31

from fastapi import FastAPI, BackgroundTasks, Depends
import time

app = FastAPI()

# lets first create a method that we are gonna call in the background.
def write_notification(email: str, message=""):
    with open('log.txt', mode='w') as email_file:
        content = f"notification for {email}: {message}"
        time.sleep(5)
        email_file.write(content)

# now, lets create our route.
@app.post("/send-notification/{email}", status_code=202)
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "notification sent in the background"}

"""
Status Code: 202
the request has been accepted for processing, but the processing has not been completed.
"""

"""
if we run the above code, in the swagger as soon as we click on 'execute', we will get 202 response.
"'message': 'notification sent in the background' will be returned as the response from API.
However, if we check the log.txt at the same time as we click or as we get the response from API, we will see nothing there.
Only, after 5 seconds, we will see 'notification for {email}: {message}' being written in the log.txt
So, the function is executed in the background even though the response is returned from the API.
"""

# now, lets look at dependency injection.
def write_log(message: str):
    with open('log.txt', mode='a') as log:   # READ ABOUT MODE 'a' AND 'w' KA DIFFERENCE(IT IS MENTIONED BELOW AS WELL)
        log.write(message)

def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q

@app.post("/send-notification/{email}")
async def send_notification(
    email: str, background_tasks: BackgroundTasks, q: str = Depends(get_query)
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent", "query": q}

"""
here, if we dont include q, we will get "'message': 'message sent', 'query': null" as the response from api
and we will get "message to {email}" in the log.txt

now, if we do include q, i.e give a value to query parameter 'q', we will get "'message': 'message sent', 'query': {q}" as response from api
and we will get "found query: {q}" and "message to {email}" in the log.txt 

if mode is 'w', it will remove existing content in file and then write.
if mode is 'a', it will add the text at the end of previous text.
"""

# BACKGROUND TASKS ARE NOT A REPLACEMENT FOR SOMETHING LIKE CELERY
# CELERY IS BETTER FOR HEAVY COMPUTATIONAL BACKGROUND TASKS OR THINGS WHERE WE DONT NEED TO SHARE PROCESSES.
# BACKGROUND TASKS ARE MORE FOR SMALLER THINGS