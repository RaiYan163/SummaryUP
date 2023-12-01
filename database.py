import sqlalchemy
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
load_dotenv()

print(sqlalchemy.__version__)




def get_engine():
    db_connection_string = os.getenv("DATABASE_URI")
    engine = create_engine(
    db_connection_string,
    connect_args={
        "ssl":{
            "ssl_ca": "/etc/ssl/cert.pem"
        }
    }
    )
    return engine

"""
engine = get_engine()

userID = 7

query = text("SELECT * FROM Summary where userID = :param_name")
query = query.bindparams(param_name=userID)

with engine.connect() as conn:
    result = conn.execute(query)

    result_dicts = []

    for row in result.all():
        temp = row._asdict()
        result_dicts.append(row._asdict())
        
        #Extract values into seperate variables
        summaryID = temp['summaryID']
        userID = temp['userID']
        urlLink = temp['urlLink']
        summaryTitle = temp['summaryTitle']
        rating = temp['rating']

        print(f"Summary ID: {summaryID}")
        print(f"User ID: {userID}")
        print(f"urlLink : {urlLink}")
        print(f"summaryTitle: {summaryTitle}")
        print(f"rating: {rating}")
        print("\n")
    #print(result_dicts)

    print(type(result_dicts))

"""