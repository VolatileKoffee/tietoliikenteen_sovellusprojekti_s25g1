# Purpose of this program: Fetches data straight from measurements -database.

import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv() # loading credentials
localhost = os.getenv("LOCALHOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")


def fetch_data_from_db():
    mydb = mysql.connector.connect(
        host=localhost,
        user= db_user,
        password= db_password,
        database=db_name
        )

    mycursor = mydb.cursor()        

    query = "SELECT * FROM rawdata ORDER BY id;"
    try:
        mycursor.execute(query)
        received_data = mycursor.fetchall()
    except:
        raise Exception("Error: unable to fetch data.") 
    
    for row in received_data:
        print(f"{row}")
    mydb.close()


if __name__ == "__main__":
    # print("Hello World!")
    fetch_data_from_db()
    