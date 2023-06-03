from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base



from typing import Optional, List
from sqlmodel import Field, Relationship, JSON, Column, SQLModel
from history.common import TimestampModel, UUIDModel
# from .user import User




class User(SQLModel, table = True):
    __tablename__ = "user"

    id: int = Field(primary_key = True, index = True)
    email: str = Field(unique = True, index = True)
    hashed_password: str  
    is_active: bool = Field (default = True)

    # items = Relationship("Item", back_populates = "owner")

# class Item(SQLModel, table = True):
#     __tablename__ = "items"

#     id =  primary_key = True, index = True)
#     title = index = True)
#     description = index = True )
#     owner_id =  ForeignKey("users.id"))

#     owner = relationship("User", back_populates = 'items')



class History(SQLModel, table = True):
    __tablename__ = "history"
    
    id: int = Field(primary_key = True, index = True)

    input: str
    result: List[str] = Field(sa_column=Column(JSON))
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

    user: Optional[User] = Relationship(back_populates="user")

    class Config:
        arbitrary_types_allowed = True
        
    # def __repr__(self):
    #     return f"<History (id: {self.id})>"

    




# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key = True, index = True)
#     email = Column(String, unique = True, index = True)
#     hashed_password = Column(String)
#     is_active = Column(Boolean, default = True)

#     items = relationship("Item", back_populates = "owner")

# class Item(Base):
#     __tablename__ = "items"

#     id = Column(Integer, primary_key = True, index = True)
#     title = Column(String, index = True)
#     description = Column(String, index = True )
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates = 'items')
