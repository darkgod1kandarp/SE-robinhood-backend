from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from  database import Base
import datetime
import uuid

  
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True),  default=uuid.uuid4   , primary_key=True)
    name = Column(String, unique=True)
    mobilenumber= Column(String)
    is_volunteer = Column(Boolean, default=True)
    password  =  Column(String)
    city  =   Column(String)
    email  =  Column(String)
    items=  relationship("FoodDetail", back_populates="owner")

class FoodDetail(Base):
    __tablename__ = "fooddetail"
    id = Column(UUID(as_uuid=True),  default=uuid.uuid4   , primary_key=True)
    owner_id  = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    location  =  Column(String)
    created_at  =  Column(DateTime, default  =  datetime.datetime.utcnow)
    owner = relationship("User", back_populates="items")
    is_delivered =  Column(Boolean, default=False)
    shared_food  =  relationship("SharedFood" , back_populates="user_food")
    
class SharedFood(Base):
    __tablename__= "sharedfood"
    id = Column(UUID(as_uuid=True),  default=uuid.uuid4   , primary_key=True)
    foodname =  Column(String)
    quantity = Column(String)
    details_id  = Column(UUID(as_uuid=True), ForeignKey("fooddetail.id"))
    user_food  =  relationship("FoodDetail" , back_populates="shared_food")
    
        
    
    

