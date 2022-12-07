from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import os
import operation as operation, models as models, schema as schema
from database import SessionLocal, engine
from typing import Any
from fastapi import FastAPI
import socketio
sio: Any = socketio.AsyncServer(async_mode="asgi" ,  cors_allowed_origins='*')
socket_app = socketio.ASGIApp(sio)

models.Base.metadata.create_all(bind=engine)

# app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# @app.post("/SignUp/user", response_model=schema.UserBase)
# def create_user(user: schema.CreateUser, db: Session = Depends(get_db)):
#     if operation.find_user(db,user.name ):
#         raise HTTPException(status_code=400, detail="User already exist")
#     return operation.create_user(db=db, user_data=user)

# @app.post("/SignIn/user" )
# def login_user(user :schema.Login , db: Session = Depends(get_db)):
   
#     data  = operation.login_user(db , user)
#     if not data :
#         raise HTTPException(status_code=400, detail  = "Invalid username or password")
#     return data.id
# @app.post("/user/foodshare")
# def food_share(food :schema.FoodDetail , db: Session = Depends(get_db) ):
#     data  =  operation.store_data(db  ,  food)
#     if not data:
#         raise HTTPException(status_code=400, detail = "Invalid argument")
#     return  "data has been stored"

# @app.get("/shared/{id}" , response_model = List[schema.UserFoodDetail])
# def user_food_share( id:str, db: Session = Depends(get_db)):
#     print(operation.shared_food_data(db ,  id) )
#     # print(operation.shared_food_data(db ,  id).shared_food[0].__dict__  )
#     return operation.shared_food_data(db ,  id)  

# # app.mount("/", socket_app)

# # @sio.event
# # async def connect(sid  , env):
# #     print("on connect")
    
# # # # @sio.on("")
    
    



# if __name__=='__main__':
#     os.system('uvicorn main:app --host 10.1.157.173  --port 9000 --reload')

from typing import Any
from urllib import response

import uvicorn
from fastapi import FastAPI
import socketio

sio: Any = socketio.AsyncServer(async_mode="asgi" , cors_allowed_origins='*')
socket_app = socketio.ASGIApp(sio)
app = FastAPI()


@app.get("/test")
async def test():
    print("test")
    return "WORKS"

@app.post("/SignUp/user", response_model=schema.UserBase)
def create_user(user: schema.CreateUser, db: Session = Depends(get_db)):
    print(user)
    if operation.find_user(db,user.name ):
        raise HTTPException(status_code=400, detail="User already exist")
    return operation.create_user(db=db, user_data=user)

@app.post("/SignIn/user" )
def login_user(user :schema.Login , db: Session = Depends(get_db)):
   
    data  = operation.login_user(db , user)
    if not data :
        raise HTTPException(status_code=400, detail  = "Invalid username or password")
    return data.id
# @app.post("/user/foodshare")
# def food_share(food :schema.FoodDetail , db: Session = Depends(get_db) ):
#     data  =  operation.store_data(db  ,  food)
#     if not data:
#         raise HTTPException(status_code=400, detail = "Invalid argument")
#     return  "data has been stored"

@app.get("/shared/{id}" , response_model = List[schema.UserFoodDetail])
def user_food_share( id:str, db: Session = Depends(get_db)):
    print(operation.shared_food_data(db ,  id) )
   
    return operation.shared_food_data(db ,  id)  




app.mount("/", socket_app)  # Here we mount socket app to main fastapi app


@sio.on("connect")
async def connect(sid, env):
    print("on connect")


@sio.on("direct")
async def direct(sid, msg):
    print(f"direct {msg}")
    await sio.emit("event_name", msg, room=sid)  # we can send message to specific sid


@sio.on("join")
async def broadcast(sid, msg):
    msg  =  msg['food']
   
    data  =  operation.store_data( Depends(get_db)   ,  msg )
    if not data:
        raise HTTPException(status_code=400, detail = "Invalid argument")
    return  "data has been stored"
    
    


    

   

    
    # await sio.emit("ev", msg)  # or send to everyone


@sio.on("disconnect")
async def disconnect(sid):
    print("on disconnect")
    



if __name__ == "__main__":
    kwargs = {"host": "0.0.0.0", "port": 5000}
    kwargs.update({ "reload": True})
    uvicorn.run("main:app", **kwargs)
