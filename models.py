from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime , Enum
from sqlalchemy.orm import relationship
from  database import Base
import datetime
import uuid
import enum


class MyEnum(enum.IntEnum):
    delivering = 1
    delivered = 2
    pending= 3
  
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True),  default=uuid.uuid4   , primary_key=True)
    name = Column(String)
    mobilenumber= Column(String)
    is_volunteer = Column(Boolean, default=True)
    password  =  Column(String)
    city  =   Column(String)
    email  =  Column(String , unique=True)
    items=  relationship("FoodDetail", back_populates="owner")
    status =  relationship("FoodStatus" , back_populates="users")


class FoodDetail(Base):
    __tablename__ = "fooddetail"
    id = Column(UUID(as_uuid=True),  default=uuid.uuid4   , primary_key=True)
    owner_id  = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    location  =  Column(String)
    created_at  =  Column(DateTime, default  =  datetime.datetime.utcnow)
    owner = relationship("User", back_populates="items")
    is_delivered =  Column(Enum(MyEnum), default=MyEnum.pending)
    quantity =   Column(String)
    description =   Column(String)
    shared_food  =  relationship("FoodStatus" , back_populates="foodies", uselist=False)

class FoodStatus(Base):
    __tablename__= "foodstatus"
    id = Column(UUID(as_uuid=True),  default=uuid.uuid4   , primary_key=True)
    foodid  = Column(UUID(as_uuid=True), ForeignKey("fooddetail.id"))
    volunteerid  =   Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at  =  Column(DateTime, default  =  datetime.datetime.utcnow)
    foodies  =  relationship("FoodDetail"  , back_populates  = "shared_food" , uselist=False)
    users  =  relationship("User" , back_populates="status" , uselist=False)
    
    
          
    
    

