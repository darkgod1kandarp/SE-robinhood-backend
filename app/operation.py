from sqlalchemy.orm import Session
from sqlalchemy import and_
import models as models, schema as schema
import uuid

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

    return db_user.__dict__

def list_food(db:Session  ):
    
    return db.query(models.FoodDetail).filter()

def  login_user(db: Session , user_data :schema.LoginUser):
  
    return db.query(models.User).filter(and_(models.User.email ==  user_data.email , models.User.password==user_data.password) ).first()

def find_user(db  :Session ,  email : str ):

    return db.query(models.User).filter(models.User.email ==  email).first()

def find_user_by_id(db : Session ,  userid :  str):
    return db.query(models.User).filter(models.User.id ==  userid).first()

def store_data(db:Session ,user_data):
    
   
    try  :  
        db_order  =  models.FoodDetail(
                            owner_id=user_data['owner_id'],
                            location  =   user_data['location'],
                            quantity =   user_data['quantity'], 
                            description =  user_data['description']
                            )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        
    except Exception as ex : 
        print(ex)
        return False
    return db_order.__dict__
def shared_food_data(db:Session , userid:str):
    return db.query(models.FoodDetail).filter(models.FoodDetail.owner_id == userid).all()

def storing_food(db:Session  , msg ):

    try:
        print(msg)
        val  =  db.query(models.FoodStatus).filter(and_(models.FoodStatus.foodid==uuid.UUID(msg['foodid']) , models.FoodStatus.volunteerid==uuid.UUID(msg['volunteer_id']))).first()
        print(val)
        if not val  :
            db_order  =   models.FoodStatus(
                foodid   = uuid.UUID(msg['foodid']) ,  
                volunteerid =  uuid.UUID(msg['volunteer_id'])
            )
            db.add(db_order)
            db.commit()
           
       
        
       
        
    except Exception as ex:
      
        return False 
    return True

def updating_conversion(db:Session ,  msg):
    try:
        updating =   db.query(models.FoodDetail).filter(models.FoodDetail.id ==   msg['foodid'])
        updating_data  =  updating.first()
        updating_data.is_delivered =  1
        val  =  updating_data.__dict__ 
        del  val['_sa_instance_state']
        updating.update(val)
        db.commit()
       
    except Exception as ex:
        print(False,ex)

def volunteer_opertation(db:Session ,  msg):
    try:
        volunteer  =   db.query(models.FoodStatus).filter(models.FoodStatus.volunteerid ==msg['user_id'])
        data  =   []
        for  value  in  volunteer:
            food_data  =   db.query(models.FoodDetail).filter(and_(models.FoodDetail.id ==value.foodid ,models.FoodDetail.is_delivered=="delivering")).first() 
            if food_data:
                data.append({'name':food_data.owner.name , 'description':food_data.description,
                            
                                'location':food_data.location,
                                'quantity' :food_data.quantity, 
                                'created_at':str(food_data.created_at) ,  
                                'id':str(food_data.id) 
                                
                            })
  
        return data
            
    except Exception as ex:
        print(ex)
        return False
    
def changing_food_status(db:Session , msg):
    try:
        if msg['state']==0:
            updating =   db.query(models.FoodDetail).filter(models.FoodDetail.id ==   msg['food_id'])
            updating_data  =  updating.first()
            updating_data.is_delivered =  3
            val  =  updating_data.__dict__ 
            del  val['_sa_instance_state']
            updating.update(val)
     
            db.commit()
            db.refresh(val)
        else:
            updating =   db.query(models.FoodDetail).filter(models.FoodDetail.id ==   msg['food_id'])
            updating_data  =  updating.first()
            updating_data.is_delivered =  2
            val  =  updating_data.__dict__ 
            del  val['_sa_instance_state']
            updating.update(val)
            db.commit()
            db.refresh(val)
            
           
    except Exception as ex:
        return False

def changing_volunteer_status(db:Session   ,  msg):
    try:
        if msg['state']==0:
            db.query(models.FoodStatus).filter(and_(models.FoodStatus.foodid ==   msg['food_id'] ,  models.FoodDetail.volunteerid==msg['user_id'])).delete()
            db.commit()

            
            
            
    except Exception as ex:
        return False
    
def giving_volunteer_complete_data(db:Session ,  msg):
    try:
        volunteer  =   db.query(models.FoodStatus).filter(models.FoodStatus.volunteerid ==msg['user_id'])
        data  =   []
        for  value  in  volunteer:
            food_data  =   db.query(models.FoodDetail).filter(and_(models.FoodDetail.id ==value.foodid ,models.FoodDetail.is_delivered=="delivered")).first() 
            if food_data:
                data.append({'name':food_data.owner.name , 'description':food_data.description,
                            
                                'location':food_data.location,
                                'quantity' :food_data.quantity, 
                                'created_at':str(food_data.created_at) ,  
                                'id':str(food_data.id) 
                                
                            })
  
        return data
            
    except Exception as ex:
        print(ex)
        return False
        

        
    


    
    



    
    