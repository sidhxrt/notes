# SECURITY -- LECTURE 26

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}

# so if we run this on server, we will have to input username-password combo, but it will not authorize coz we dont have anything to check it against(i.e a db of username-passowrd combo)

# NOW
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disable: bool | None = None

def fake_decode_token(token):
    return User(
        username=f"{token}fakedecoded", email="foo@example.com", full_name="foo bar"
    )

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user

@app.get("/users/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

# its still not gonna work bcoz we dont have any users, against which we can validate.


# so

fake_users_db = {
    "johndoe": dict(
        username="johndoe",
        full_name="John Doe",
        email= "johndoe@example.com",
        hashed_password="fakehashedsecret",
        disabled=False
    ),
    "alice": dict(
        username="alice",
        full_name="Alice Wonderson",
        email= "alice@example.com",
        hashed_password="fakehashedsecret2",
        disabled=True
    )
}

# now lets create a method to hash our password.
def fake_hash_password(password: str):
    return f"fakehashed{password}"

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disable: bool | None = None

class UserInDB(User):
    hashed_password: str

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def fake_decode_token(token):
    return get_user(fake_users_db, token)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled: 
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.get("/users/me")
async def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user
 
# now this is still not gonna work, bcoz we still dont have a token
# so we will create the following route:
@app.post("/token")     # this route is 'token' because in line 9 we have given tokenurl as 'token'
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="incorrect username or password")
    
    return {"access_token": user.username, "token_type": "bearer"}    # this return statement is needed for the Oauth2-password bearer and all

# now app.get("/users/me") will work
# Oauth2_scheme basically does the authorization by hitting the /token endpoint.
# it implements the logic that we have written in the token endpoint
# i.e first we will fetch username that user enters in login page(authorization page) and check if it exists in our db
# then it checks for the password(that is entered through login page), if it is same as the password associated with the username stored in our db
# if everything goes well, it returns success message(with the token), if not then it raises Http exception stating invalid username or password