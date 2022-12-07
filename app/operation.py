from sqlalchemy.orm import Session
from sqlalchemy import and_
import models as models, schema as schema


def create_user(db: Session,user_data:schema.CreateUser):
    db_user  =  models.User( 
                            email  = user_data.email , 
                            password  = user_data.password ,  
                            name   = user_data.name, 
                            mobilenumber =  user_data.mobilenumber,
                            is_volunteer =  user_data.is_volunteer , 
                            city  =  user_data.city, 
                            )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def  login_user(db: Session , user_data :schema.LoginUser):
  
    return db.query(models.User).filter(and_(models.User.email ==  user_data.email , models.User.password==user_data.password) ).first()

def find_user(db  :Session ,  email : str ):
    print(email)
    return db.query(models.User).filter(models.User.email ==  email).first()

def find_user_by_id(db : Session ,  userid :  str):
    return db.query(models.User).filter(models.User.id ==  userid).first()

def store_data(db:Session ,user_data  : schema.SharedFood):
    
   
    try  :  
        db_order  =  models.FoodDetail(
                            owner_id=user_data.owner_id,
                            location  =   user_data.location,
                            quantity =   user_data.quantity
                            )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        
    except Exception as ex : 
        return False
    return db_order  
def shared_food_data(db:Session , userid:str):
    return db.query(models.FoodDetail).filter(models.FoodDetail.owner_id == userid).all()


    
    



    
    