from utils import *


'''
Gets credentials from .env file, returns dictionary.
'''

def get_credentials():  
    # Load the app credentials from the environment so the database login
    # can be reused without hardcoding secrets in the source code.
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
    # Verify the entered credentials before opening a database session.
    creds = get_credentials()
    user_username = input("Enter username: ")
    user_passwd = input("Enter password: ")
    
    if user_username != creds["User"] or user_passwd != creds["password"]:
        print("Invalid username or password")
        raise(Exception("Invalid username or password"))
        return
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
        
'''
Takes connection tuple, and shows price based on room number.
'''

def show_price(connection_tuple):
    # Show the nightly rate for a room, with a loop that keeps asking until the
    # operator enters 0 to exit.
    if not connection_tuple:
        print("Invalid connection tuple")
        return
    cursor = connection_tuple[1]
    
    try_cursor_execute(cursor, "select * from rooms")
    rows = cursor.fetchall()
    
    while True:
        room_no = int_input("Enter the room number to check price, press 0 to exit: ")
        if room_no <= 0:
            break
        n = check_room_exists(cursor, room_no)
        if not n:
            continue
        print(f"Price of room number {room_no} is ${n[1]} per night")        
            


def update_price(connection_tuple):
    # Update a room's rate after validating the room number and the new price.
    if not connection_tuple:
            print("Invalid connection tuple")
            return
    
    cursor = connection_tuple[1]
    
    while True:
        room_no = int_input("Enter the room number to update price, press 0 to exit: ")
        if room_no <= 0:
            break
        
        if not check_room_exists(cursor, room_no):
            continue
        break
    new_price = int_input("Enter new price: ")
    try_cursor_execute(cursor, "select * from rooms")
    rows = cursor.fetchall()
    
    try_cursor_execute(cursor, "update rooms set price=%s where room_no=%s", (new_price, room_no))
    connection_tuple[0].commit()
    print(f"Price of room number {room_no} updated to ${new_price} per night")
    
        


def display_floors(connection_tuple):
    # Group rooms by floor numbers and print each floor's rooms in a neat table.
    cursor = connection_tuple[1]
    try:
        cursor.execute("select * from rooms")
        
    except:
        print("Could not fetch from database")
        return
    while True:
        # Accept a comma-separated floor list and print only the matching rooms.
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

def check_in(connection_tuple):
    # Create a booking only after confirming the room exists, is available,
    # and the stay duration is valid.
    if not connection_tuple:
        print("Invalid connection tuple")
        return
    cursor = connection_tuple[1]
    
    while True:
        room_no = int_input("Enter the room number to check in, press 0 to exit: ")
        if room_no <= 0:
            break
        n = check_room_exists(cursor, room_no)
        if not n:
            continue
        if not check_room_availability(cursor, room_no):
            continue
        name = input("Enter your name: ")
        duration = int_input("Enter duration of stay in days: ")
        if duration <= 0:
            print("Invalid duration")
            continue
        booking_id = generate_booking_id()
        try_cursor_execute(cursor, "insert into bookings values (%s, %s, %s, %s, %s)", (booking_id, room_no, name, date.today(), duration,))
        connection_tuple[0].commit()
        print(f"Checked in to room number {room_no}. Booking ID: {booking_id}")

def check_out(connection_tuple):
    # Look up the booking by ID, confirm it exists, then delete it and commit.
    if not connection_tuple:
        print("Invalid connection tuple")
        return
    cursor = connection_tuple[1]
    
    while True:
        booking_id = input("Enter the booking ID to check out, press 0 to exit: ")
        if booking_id == "0":
            break
        try_cursor_execute(cursor, "select * from bookings where booking_id=%s", (booking_id,))
        n = cursor.fetchone()
        if not n:
            print(f"Booking ID {booking_id} does not exist")
            continue
        try_cursor_execute(cursor, "delete from bookings where booking_id=%s", (booking_id,))
        connection_tuple[0].commit()
        print(f"Checked out of room number {n[1]}. Booking ID: {booking_id}")


def display_vaccant_rooms(connection_tuple):
    # Filter the room list to only those currently available and print them.
    if not connection_tuple:
        print("Invalid connection tuple")
        return
    cursor = connection_tuple[1]
    
    try_cursor_execute(cursor, "select * from rooms")
    rooms = cursor.fetchall()
    
    
    vaccant_rooms = []
    for room in rooms:
        if check_room_availability(cursor, room[0]):
            vaccant_rooms.append(room)
    
    print("Vaccant rooms:")
    print(tabulate(vaccant_rooms, headers = ("Room", "Price")))
                
    

        
