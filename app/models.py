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
    name = Column(String)
    mobilenumber= Column(String)
    is_volunteer = Column(Boolean, default=True)
    password  =  Column(String)
    city  =   Column(String)
    email  =  Column(String , unique=True)
    items=  relationship("FoodDetail", back_populates="owner")

class FoodDetail(Base):
    __tablename__ = "fooddetail"
    id = Column(UUID(as_uuid=True),  default=uuid.uuid4   , primary_key=True)
    owner_id  = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    location  =  Column(String)
    created_at  =  Column(DateTime, default  =  datetime.datetime.utcnow)
    owner = relationship("User", back_populates="items")
    is_delivered =  Column(Boolean, default=False)
    quantity =   Column(String)
    description =   Column(String)

    
    # shared_food  =  relationship("SharedFood" , back_populates="user_food")
    
# class SharedFood(Base):
#     __tablename__= "sharedfood"
#     id = Column(UUID(as_uuid=True),  default=uuid.uuid4   , primary_key=True)
#     quantity = Column(String)
#     user_food  =  relationship("FoodDetail" , back_populates="shared_food")
    
        
    
    

