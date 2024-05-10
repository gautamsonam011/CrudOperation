from fastapi import FastAPI,Depends,HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db import SessionLocal,engine
from model import Base
import schema,crud
from jose import jwt


Base.metadata.create_all(bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
app = FastAPI()


@app.post("/users/")
def add_data(user:schema.UserCreate,db:Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code = 400, detail="Email already registered")
    return crud.create_user(db = db, user=user)

@app.get("/users/")
def read_data(skip:int = 0,limit:int = 100, db:Session = Depends(get_db)):
    users = crud.get_users(db, skip = skip, limit=limit)
    return users

@app.get("/users/{user_id}")
def read_users(user_id:int, db:Session = Depends(get_db)):
    db_user = crud.get_user(db,user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not Found")
    return db_user

