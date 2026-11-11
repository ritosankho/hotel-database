import pymysql as mysql
from tabulate import tabulate
import os
from dotenv import load_dotenv
from datetime import date
import string
import random

def int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
            return -1

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

def check_room_exists(cursor, room_no):
    try_cursor_execute(cursor, f"SELECT * FROM rooms where room_no={room_no}")
    n = cursor.fetchone()
    if not n:
        print(f"Room number {room_no} does not exist")
        return None
    return n

def generate_booking_id(length=10):
    characters = string.ascii_letters + string.digits
    id = ''.join(random.choice(characters) for _ in range(length)).lower()
    return id

def check_room_availability(cursor, room_no):
    try_cursor_execute(cursor, f"SELECT * FROM bookings where room_no={room_no}")
    n = cursor.fetchone()
    if n:
        print(f"Room number {room_no} is already booked")
        return False
    
    return True

