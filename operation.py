from xml.parsers.expat import model
from sqlalchemy.orm import Session
from sqlalchemy import and_
import models, schema


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
    print(user_data.name ,  user_data.password)
    return db.query(models.User).filter(and_(models.User.name ==  user_data.name , models.User.password==user_data.password) ).first()

def find_user(db  :Session ,  username : str ):
    return db.query(models.User).filter(models.User.name ==  username).first()

def find_user_by_id(db : Session ,  userid :  str):
    return db.query(models.User).filter(models.User.id ==  userid).first()

def store_data(db:Session ,user_data  : schema.SharedFood):
    
   
    try  :  
        db_order  =  models.FoodDetail(
                            owner_id=user_data.owner_id,
                            location  =   user_data.location
                            )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        
        if len(user_data.foodname)!=len(user_data.quantity):
            return False
        for  i  in range(len(user_data.foodname)):
            
            db_item  =  models.SharedFood(
                            details_id =   db_order.id,
                            foodname  =  user_data.foodname[i],
                            quantity = user_data.quantity[i],
            )
            db.add(db_item)
            db.commit()
            db.refresh(db_item)
    except Exception as ex :
      
        return False
    
    return db  
def shared_food_data(db:Session , userid:str):
    return db.query(models.FoodDetail).filter(models.FoodDetail.owner_id == userid).all()
    
    



    
    