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
from fastapi.middleware.cors import CORSMiddleware
from pytz import timezone 
from datetime import datetime
import json
sio: Any = socketio.AsyncServer(async_mode="asgi" , cors_allowed_origins='*')
socket_app = socketio.ASGIApp(sio)
app = FastAPI()

socket_user  =   {}

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

@app.get("/test")
async def test():
    print("test")
    return "WORKS"

@app.post("/SignUp/user")
def create_user(user: schema.CreateUser, db: Session = Depends(get_db)):
    print(user)
    # print(operation.find_user(db,user.name ) ,  "er32")
    if operation.find_user(db,user.email ):
        raise HTTPException(status_code=400, detail="User already exist")
    return operation.create_user(db=db, user_data=user)

@app.post("/SignIn/user" )
def login_user(user :schema.Login , db: Session = Depends(get_db)):
   
    data  = operation.login_user(db , user)
    # # first data
    # print(data.__dict__)
    if not data :
        raise HTTPException(status_code=400, detail  = "Invalid username or password")
    return data.__dict__


@app.get("/shared/{id}" , response_model = List[schema.UserFoodDetail])
def user_food_share( id:str, db: Session = Depends(get_db)):
    print(operation.shared_food_data(db ,  id) )
   
    return operation.shared_food_data(db ,  id)  




app.mount("/", socket_app)  # Here we mount socket app to main fastapi app


@sio.on("connect")
async def connect(sid, env):
  
   print("connected")


@sio.on("direct")
async def direct(sid, msg):
    print(f"direct {msg}")
    await sio.emit("", msg, room=sid)  # we can send message to specific sid


@sio.on("join")
async def broadcast(sid, msg):
    if msg!=False:
        data  =  operation.store_data( next(get_db())   ,  msg )
        await sio.emit("check", True if  data else False , room  = sid )


        
    food_list_data =  operation.list_food(next(get_db()) )
    food_list_data_list =   []
    for  food  in food_list_data:
        time1  = datetime.now(timezone("Asia/Kolkata")).strftime(food.created_at.strftime('%Y:%m:%d %H:%M:%S %Z %z'))
        if json.dumps(food.is_delivered )!=2:
            food_list_data_list.append({'id':str(food.id) ,  "owner_id":str(food.owner_id) ,  "location":food.location  , "created_at": time1 , "is_delivered" :  json.dumps(food.is_delivered ),  "quantity"  :  food.quantity ,  "description" : food.description })
        
    

    await sio.emit("after" ,  food_list_data_list[::-1] )
    
@sio.on("converting")
async def catching(sid ,  msg) :
    # is_deilivered update karvanu che and 
    # store karvanu che food_id ,  volunteer_id 
 
    operation.storing_food(next(get_db()) , msg)
    operation.updating_conversion(next(get_db()) ,  msg)

@sio.on("volunteerfood")
async def volunteer(sid  ,  msg):
    
    data = operation.volunteer_opertation(next(get_db()), msg)
    if data:
        await sio.emit('accepted' ,  data)
    else:
        await sio.emit('accepted' , False)
    
@sio.on("reject_accept")
async def function(sid ,  msg):
  
    operation.changing_food_status(next(get_db()) , msg)
    operation.changing_volunteer_status(next(get_db()) ,  msg)



@sio.on("delivered")
async def function1(sid ,msg):
  
    data  =  operation.giving_volunteer_complete_data(next(get_db()) ,  msg )
    if data  :
        await sio.emit("delivered_data" ,  data)
    else:
        await sio.emit("delivered_data" , False)
        
@sio.on("user_donor")
async def function2(sid  , msg):
    await sio.emit("user_donor_data"  ,operation.giving_user_order( next(get_db()) ,  msg)  )
    

   
    
    
    
    
    
        
    
    

@sio.on("disconnect")
async def disconnect(sid):
    print("on disconnect")
    



if __name__ == "__main__":
    kwargs = {"host": "0.0.0.0" , "port": 5000}
    kwargs.update({ "reload": True})
    uvicorn.run("main:app", **kwargs)
