# SECURITY WITH JWT -- LECTURE 27

# in the last lecture, we were passing username as the token which is extraordinarily insecure.
# so now we will be working with json web token(jwt) instead of username

# additional requirements for this lecture: python-jose[cryptography] & passlib[bcrypt]

from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

app = FastAPI()


# first, lets setup the hashing algorithm and required parameters that we are gonna be using.
SECRET_KEY = "thequickbrownfoxjumpsoverthelazydog"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = dict(
    johndoe=dict(
        username="johndoe",
        full_name="John Doe",
        email = "johndoe@example.com",
        hashed_password="$2b$12$dVZfGpH0tFnIY6wxswOuU.fgf/ZDDDrTv4LrY2HWxGGGscRj8DQKi",
        disabled=False
    )
)

# this below scheme(format inside the class) is needed for Oauth2 password-bearer and all 
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str 
    email: str | None = None
    full_name: str | None = None
    disabled: bool = False

class UserInDB(User):
    hashed_password: str 

"""
now,
we need to setup a password context 
and what this is going to do is, 
this is going to give us functionality where we can hash passwords, 
we can verify passwords and things like that.
"""

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # we can check docs of passlib-context(then search for schemes and then deprecated)
# from the docs, we got to know that, schemes is a list of algorithms which the instance( of CryptContext class) should support.
# from the docs, we got to know that, deprecated is a list of algorithms which should be considered "deprecated"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# when we go to authorize button as seen on fastapi tutorials, it will call this 'token' url

# now we will set up some helper functions
def verify_password(plain_password, hashed_password):  
# this will take a plain password that we are gonna use to login and its gonna compare it against a hashed password thats in the fake_users_db
    return pwd_context.verify(plain_password, hashed_password)
 
"""
we are not gonna be storing plain text passwords in the database, thats not a good thing to do.
we will be storing hashed passwords in the database.
but then how will we be checking to make sure that the password is valid?
we do something like this:
we gonna pass in the plain password, which will use the algorithms that we have set and the parameters that we have set
and it will hash it and it will check to see that if they are equal.
"""

# now
def get_password_hash(password):
    return pwd_context.hash(password)

# the above 2 are helper methods, we dont have to worry too much about where we are gonna be using them. we will figure that out later

# now
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
# what the above method is doing is we are passing in a value with our db, so we would pass in johndoe with our fake_users_db 
# and if that user is in the database, we are gonna create a UserInDB object where we will get the 4 fields of class User and the hashed password of class UserInDB

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)   # if user(associated with the username) doesnt exist,  get_user() will return nothing
    if not user:   
        return False
    if not verify_password(password, user.hashed_password):   # if password doesnt match, then it will return False
        return False
    return user

# when we pass the access_token information(defined in the /token post request) this method will return jwt
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt

# now lets setup our token route, the route that will return our token
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # now what we gonna do is we gonna create a token that will expire after a certain period of time.
    # the way access tokens work with json web tokens is typically we are going to have an access token thats passed in as a header,
    # its a bearer token that is then verified by any protected routes that we have.
    # we will also get a refresh token; once our access token expires, we then submit a post request with that refresh token and we get a new access token.
    # and sometimes we will rotate the refresh token and stuff like that. concept of refresh token is lil complex to code, hence skipped in this lecture. 
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

"""
to generate hash of a password-
go to IDLE and type the following code:

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
pwd_context.hash('password1234')

>> this will give 'hashed password' of our 'input password' as output
"""

# DONT PASS SENSITIVE DATA IN OUR JWT PAYLOAD

# now we will first take in the token thats passed in via the oauth2_scheme, then we will decode the token
# then we will get the username from the token, then we will get the user from the token(i.e we will check if the user is in the database)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # firstly, we gonna have few unauthorized exception that can get thrown, so lets first just create the exception
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        # decoding the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # fetching the username
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    # fetching the user from db(fake_users_db)
    user = get_user(fake_users_db, username=token_data.username) # we can write this also: get_user(fake_users_db, username=username), as we have already fetched username at line 159
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive User")
    return current_user

# now lets create routes that are protected:
@app.get("/users/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "foo", "owner": current_user.username}]
