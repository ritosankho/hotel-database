import pymysql as mysql
from tabulate import tabulate
import os
from dotenv import load_dotenv
from datetime import date
import string
import random

# Loads credentials and database settings from environment variables.
def get_credentials():  
    try:
        load_dotenv()
        operator = os.environ["OPERATOR"]
        password = os.environ["DB_PASSWORD"]
        
        admin_passwd = os.environ["ADMIN_PASSWORD"]
        host = os.environ["HOST"]
        db = os.environ["DBNAME"]
        return {"User":operator,"db":db, "host": host, "password":password, "admin_passwd":admin_passwd}
        
    except:
        print("Cannot access database credentials. Check environment variables")
 
# Opens the database connection after credential validation.
def connect():   
    creds = get_credentials()
    
    try:
        connection = mysql.connect(host = creds["host"],
                            user =creds["User"] ,
                            password=creds["password"],
                            database = creds["db"])
        print("Connected to database")
        cursor = connection.cursor()
        return (connection,cursor)
    except Exception as e:
        ("Failed to connect to database")
        print(e)

# Reads and validates an integer from the user.
def int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
            return -1

# Executes a database query and reports errors.
def try_cursor_execute(cursor, query, params=None):
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return True
    except mysql.Error as e:
        print(f"Database error: {e}")
        return False

# Finds a room by its room number.
def check_room_exists(cursor, room_no):
    try_cursor_execute(cursor, f"SELECT * FROM rooms where room_no={room_no}")
    n = cursor.fetchone()
    if not n:
        print(f"Room number {room_no} does not exist")
        return None
    return n

# Generates a random booking identifier.
def generate_booking_id(length=10):
    characters = string.ascii_letters + string.digits
    id = ''.join(random.choice(characters) for _ in range(length)).lower()
    return id

# Checks whether a room already has a booking.
def check_room_availability(cursor, room_no):
    try_cursor_execute(cursor, f"SELECT * FROM bookings where room_no={room_no}")
    n = cursor.fetchone()
    if n:
        print(f"Room number {room_no} is already booked")
        return False
    
    return True

# Generates the next customer or employee ID.
def generate_id(connection_tuple, id_user = "customer"):
    if id_user.lower() == "customer":
        table = "customer"
        id_string = "cust"
    elif id_user.lower() == "employee":
        table = "employees"
        id_string = "emp"
    cursor = connection_tuple[1]
    
    try_cursor_execute(cursor, f"select count(*) from {table}")
    last_person = cursor.fetchone()[0]
    current_person = last_person+1
    no_of_zeros = 6 - len(str(current_person))
    id = id_string + "0"*no_of_zeros + str(current_person)
    return id
