from sqlalchemy.orm import Session

from . import models, schemas

# This is a test comment
# update test comment

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyHashed"
    new_user = models.User(email = user.email, hashed_password = fake_hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



def get_item(db: Session, id: int):
    return db.query(models.Item).filter(models.Item.id == id).first()

def get_items(db: Session, skip: int = 0 , limit: int = 50):
    return db.query(models.Item).offset(skip).limit(limit).all() 

def create_item(db: Session, item: schemas.ItemCreate, user_id: int):
    new_item = models.Item(**item.dict(), owner_id = user_id)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item