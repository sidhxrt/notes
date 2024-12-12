# 004 starts

from sqlalchemy.orm import Session
from . import models, schemas

# now we are going to create some methods to get the users (by their emails or id or something)
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# now lets write a function to get multiple users
def get_users(db: Session, skip: int = 0, limit: int = 100):
    # the below code will get us all the users in the database
    # return db.query(models.User).all()
    # to get users from lets say 20(for 20, make skip=20 instead of 0 above) to 100, we will use offset and limit
    return db.query(models.User).offset(skip).limit(limit).all()

# now lets write a function to fetch our items
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

# now lets write a function to create user
# querying database is done with the above functions
# now we will be creating stuffs in the db
# we will be instantiating an object, adding it to database and committing it.
def create_user(db: Session, user: schemas.UserCreate):
    # first, we will creat the hashed password
    fake_hashed_password = user.password + "notreallyhashed"    
    # now, we need to create a User instance (from our models.py)
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    # the User in the above line is the one from the database(models.py) and not schemas.py

    # we have created the database instance for the table(db_user is the instance)
    db.add(db_user)
    # by doing db.commit(), we are saving the instance to the database.
    db.commit()
    # by doing db.commit(), it also creates the primary key, id value, etc
    # but we dont actually have that until we call db.refresh()
    # db.refresh() will add the id to the db_user instance
    db.refresh(db_user)
    return db_user


# similarly, lets write a function to create user item
def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# 004 ends