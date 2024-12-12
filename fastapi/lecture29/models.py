# 002 starts

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    # setting up the tablename
    __tablename__ = 'users'

    # setting up our fields/columns ( each of these properties of the class will be a column in the database )
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)  # we want to be able to search either by id or by email, hence index=True
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")
    # relationship creates either many to many relationship or one to many relationship (<more context needed here>)

# index=True is really just for anything that we want to be able to search the database on.

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
 
# 002 ends