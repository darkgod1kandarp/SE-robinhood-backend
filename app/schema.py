from typing import List, Union
from pydantic import BaseModel
from uuid import UUID
import datetime

class UserBase(BaseModel):
    name :str
    mobilenumber:str
    is_volunteer:bool
    password:str
    city:str
    email:str
    
    class Config:
        orm_mode = True
class CreateUser(UserBase):
 
    pass
class  Login(BaseModel):
    email:str  
    password:str
    class Config:
        orm_mode = True

class  LoginUser(Login):
    pass

class  FoodDetail(BaseModel):
    owner_id : UUID 
    location:str
    quantity:str
    class Config:
        orm_mode = True


# class DataFood (BaseModel):
    


class SharedFood(FoodDetail):
    pass

class SharedFoodDetail(BaseModel):
    id :UUID
    foodname:str
    quantity :str
    details_id  :UUID
    class Config:
        orm_mode = True
    
    
class UserFoodDetail(BaseModel):
    id :UUID
    owner_id:UUID
    location :str
    created_at :datetime.datetime
    is_delivered :bool
    shared_food :List[SharedFoodDetail] 
    class Config:
        orm_mode = True
# class UserListFoodDetail(BaseModel):
#     data:List[UserFoodDetail]
#     class Config:
#         orm_mode = True
  
    
    

    
    