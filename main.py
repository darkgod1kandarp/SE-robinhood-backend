from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import os
import operation, models, schema
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = [
"*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.post("/SignUp/user", response_model=schema.UserBase)
def create_user(user: schema.CreateUser, db: Session = Depends(get_db)):
    if operation.find_user(db,user.name ):
        raise HTTPException(status_code=400, detail="User already exist")
    return operation.create_user(db=db, user_data=user)

@app.post("/SignIn/user" )
def login_user(user :schema.Login , db: Session = Depends(get_db)):
   
    data  = operation.login_user(db , user)
    if not data :
        raise HTTPException(status_code=400, detail  = "Invalid username or password")
    return data.id
@app.post("/user/foodshare")
def food_share(food :schema.FoodDetail , db: Session = Depends(get_db) ):
    data  =  operation.store_data(db  ,  food)
    if not data:
        raise HTTPException(status_code=400, detail = "Invalid argument")
    return  "data has been stored"

@app.get("/shared/{id}" , response_model = List[schema.UserFoodDetail])
def user_food_share( id:str, db: Session = Depends(get_db)):
    print(operation.shared_food_data(db ,  id) )
    # print(operation.shared_food_data(db ,  id).shared_food[0].__dict__  )
    return operation.shared_food_data(db ,  id)  

if __name__=='__main__':
    os.system('uvicorn main:app --host 127.0.0.1 --port 8000 --reload')
