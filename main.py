from typing import List
from fastapi import Depends, FastAPI, HTTPException
from pytz import timezone
from sqlalchemy.orm import Session
import operation as operation, models as models, schema as schema
from database import SessionLocal, engine
from typing import Any
from fastapi import FastAPI
import socketio
import json
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn

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
  
    if operation.find_user(db,user.email ):
        raise HTTPException(status_code=400, detail="User already exist")
    return operation.create_user(db=db, user_data=user)

@app.post("/SignIn/user" )
def login_user(user :schema.Login , db: Session = Depends(get_db)):
   
    data  = operation.login_user(db , user)
 
    if not data :
        raise HTTPException(status_code=400, detail  = "Invalid username or password")
    return data.__dict__


@app.get("/shared/{id}" , response_model = List[schema.UserFoodDetail])
def user_food_share( id:str, db: Session = Depends(get_db)): 
    return operation.shared_food_data(db ,  id)  


socket_data  = {}

app.mount("/", socket_app)  # Here we mount socket app to main fastapi app


@sio.on("connect")
async def connect(sid, env):
  
   print("connected")
   
@sio.on("sended")   
async def takingUserid(sid  ,  msg):
   
    socket_data[msg['user_id']] =  sid
    print(socket_data)


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
    print(socket_data , 'wefewf')
    print(socket_data , 'wefewf' , msg)
    if socket_data.get(msg['user_id'] )!=None:
        await sio.emit("user_donor_data"  ,operation.giving_user_order( next(get_db()) ,  msg) , room =   socket_data[msg['user_id']] )

            


@sio.on("disconnect")
async def disconnect(sid):
    print("on disconnect")
    



if __name__ == "__main__":
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


# {
#     "mobilenumber": "string",
#     "id": "b44cd3b6-7583-4975-be30-615c3c11d3e2",
#     "password": "string",
#     "email": "striwqwfwqfqwng",
#     "name": "string",
#     "is_volunteer": true,
#     "city": "string"
# }