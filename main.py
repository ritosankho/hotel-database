import mysql.connector
from tabulate import tabulate
import os
from dotenv import load_dotenv
from datetime import date

'''
Gets credentials from .env file, returns dictionary.
'''

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
 

'''
Authenticates user and connects to database. If the credentials given by the user
matches the .env file, it lets the user in. Returns connection tuple,
in the form (connection, cursor). The connection has to be returned from the 
function so that it does not close once it goes out of scope
'''
       
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
        return (connection,cursor)
    except Exception as e:
        ("Failed to connect to database")
        print(e)
        
'''
Takes connection tuple, and shows price based on room number.
'''

def show_price(connection_tuple):
    if not connection_tuple:
        print("Invalid connection tuple")
        return
    cursor = connection_tuple[1]
    
    try:
        cursor.execute("select * from rooms")
        rows = cursor.fetchall()
    except:
        print("Could not fetch data from the database")
    
    while True:
        try:
            room_no = int(input("Enter the room number. Enter 0 to quit "))
            if room_no == 0:
                break
        except ValueError:
            print("Enter valid numbers only")
            continue
    
        for i in rows:
            if i[0] == room_no:
                print(f"The price of the room is ${i[1]} per night")
                break
        else:
            print(f"Room number {room_no} does not exist")
            
        
            


def update_price(connection_tuple):
    if not connection_tuple:
            print("Invalid connection tuple")
            return
    
    cursor = connection_tuple[1]    
    while True:
            try:
                room_no = int(input("Enter the room number, press 0 to exit: "))
                if room_no ==0:
                    break
                new_price = int(input("Enter new price: "))
                
            except ValueError:
                print("Enter valid numbers only")
                continue
    try:
        cursor.execute("select room_no from rooms")
        for i in cursor.fetchall():
            if i[0]==room_no:
                break
        else:
            print(f"Room number {room_no} does not exist")
            return
    except:
        print("Could not read the database.")
        return
    try:
        cursor.execute("update rooms set price = %s where room_no = %s",(new_price, room_no))
    except:
        print("Could not update the database")
        


def display_floors(c):
    cursor = c[1]
    try:
        cursor.execute("select * from rooms")
        
    except:
        print("Could not fetch from database")
        return
    while True:
        floors = eval(input("Enter the floors, separated by comma. Enter 0 to exit"))
        if floors == 0:
            break
        printlst = []
        data = cursor.fetchall()
        for i in floors:
                    for j in data:
                        if j[0] >= i*100 and j[0] < (i+1)*100:
                            printlst.append(j)
                    print(f"Floor {i}")
                    print(tabulate(printlst, headers = ("Room", "Price")))
                    printlst = []
                
    
        
c = connect()

display_floors(c)