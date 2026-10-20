import mysql.connector
from tabulate import tabulate
import os
from dotenv import load_dotenv

def get_credentials():
    try:
        load_dotenv()
        operator = os.environ["OPERATOR"]
        password = os.environ["PASSWORD"]
        host = os.environ["HOST"]
        db = os.environ["DBNAME"]
        return {"User":operator,"db":db, "host": host, "password":password}
        
    except:
        print("Cannot access database credentials. Check environment variables")
        
def connect():
    creds = get_credentials()
    user_username = input("Enter username: ")
    user_passwd = input("Enter password: ")
    if user_username != creds["User"] or user_passwd != creds["password"]:
        print("Invalid username or password")
        return
    try:
        connection = mysql.connector.connect(host = creds["host"],
                            user =creds["User"] ,
                            password=creds["password"],
                            database = creds["db"])
        print("Connected to database")
        cursor = connection.cursor()
        return cursor
    except Exception as e:
        ("Failed to connect to database")
        print(e)
        
