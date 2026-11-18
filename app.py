from utils import *


# Handles room, booking, and employee operations.
def show_price(connection_tuple):
    # Displays a room's nightly rate.
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
            


# Updates a room's nightly rate.
def update_price(connection_tuple):
    # Validates the room and saves the new price.
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
    
        


# Lists rooms grouped by floor.
def display_floors(connection_tuple):
    # Prints matching rooms for requested floors.
    cursor = connection_tuple[1]
    try:
        cursor.execute("select * from rooms")
        
    except:
        print("Could not fetch from database")
        return
    while True:
        # Accepts a comma-separated floor list.
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

# Creates a room booking.
def book(connection_tuple):
    # Checks availability, then inserts a booking.
    if not connection_tuple:
        print("Invalid connection tuple")
        return
    cursor = connection_tuple[1]
    
    while True:
        room_no = int_input("Enter the room number to book, press 0 to exit to main menu: ")
        if room_no <= 0:
            break
        n = check_room_exists(cursor, room_no)
        if not n:
            continue
        if not check_room_availability(cursor, room_no):
            continue
        name = input("Enter The boarder's name: ")
        duration = int_input("Enter duration of stay in days: ")
        if duration <= 0:
            print("Invalid duration")
            continue
        booking_id = generate_booking_id()
        try_cursor_execute(cursor, "insert into bookings values (%s, %s, %s, %s, %s)", (booking_id, room_no, name, date.today(), duration,))
        connection_tuple[0].commit()
        print(f"Checked in to room number {room_no}. Booking ID: {booking_id}")

# Cancels a booking by booking ID.
def cancel_booking(connection_tuple):
    # Deletes a confirmed booking.
    if not connection_tuple:
        print("Invalid connection tuple")
        return
    cursor = connection_tuple[1]
    
    while True:
        booking_id = input("Enter the booking ID to cancel, press 0 to exit: ")
        if booking_id == "0":
            break
        try_cursor_execute(cursor, "select * from bookings where booking_id=%s", (booking_id,))
        n = cursor.fetchone()
        if not n:
            print(f"Booking ID {booking_id} does not exist")
            continue
        try_cursor_execute(cursor, "delete from bookings where booking_id=%s", (booking_id,))
        connection_tuple[0].commit()
        print(f"Cancelled the booking of room number {n[1]}. Booking ID: {booking_id}")


# Displays rooms that are not currently booked.
def display_vaccant_rooms(connection_tuple):
    # Filters and prints available rooms.
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

# Looks up and prints booking details.
def show_booking_details(connection_tuple):
    if not connection_tuple:
        print("Invalid connection tuple")
        return
    cursor = connection_tuple[1]
    while True:
        booking_id = input("Enter the booking ID to view details, press 0 to exit: ")
        if booking_id == "0":
            break
        try_cursor_execute(cursor, "select * from bookings where booking_id=%s", (booking_id,))
        n = cursor.fetchone()
        if not n:
            print(f"Booking ID {booking_id} does not exist")
            continue
        print(f"Booking ID: {n[0]}")
        print(f"Room Number: {n[1]}")
        print(f"Guest Name: {n[2]}")
        print(f"Check-in Date: {n[3]}")
        print(f"Duration of Stay: {n[4]} days")


# Displays every booking in a table.
def show_all_bookings(connection_tuple):
    if not connection_tuple:
        print("Invalid connection tuple")
        return

    cursor = connection_tuple[1]
    if not try_cursor_execute(cursor, "select * from bookings"):
        return

    bookings = cursor.fetchall()
    if not bookings:
        print("No bookings found.")
        return

    print(tabulate(
        bookings,
        headers=("Booking ID", "Room Number", "Guest Name", "Check-in Date", "Duration")
    ))
    
        
