from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://doadmin:AVNS_afezvE_jBMdHv9R_HpP@textminr-db-do-user-10431390-0.c.db.ondigitalocean.com:25060/textminr?sslmode=require"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
