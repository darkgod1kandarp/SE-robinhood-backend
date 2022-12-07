from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


print("sgrwg")
SQLALCHEMY_DATABASE_URL = "postgresql://kepbwako:Brts3eh5HoOEhXG_ncXcmnjVnRIK_0ge@rosie.db.elephantsql.com/kepbwako"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
