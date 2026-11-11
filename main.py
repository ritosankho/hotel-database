from utils import *


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

show_price(c)