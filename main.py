from app import *

def print_menu():
    print("Hotel Management System - Receptionist Dashboard")
    print("===============================================")
    print("Main Menu:")
    print("1. Show Price of a Room")
    print("2. Update Price of a Room")
    print("3. Display Rooms by Floor")
    print("4. Check In")
    print("5. Check Out")
    print("6. Exit")

def home():
    try:
        connection_tuple = connect()
    except Exception as e:
        print("Failed to connect to database.")
        print(e)
        return

    
    while True:
        print_menu()
        choice = int_input("Enter your choice (1-6): ")
        if choice == 1:
            show_price(connection_tuple)
        elif choice == 2:
            update_price(connection_tuple)
        elif choice == 3:
            display_floors(connection_tuple)
        elif choice == 4:
            check_in(connection_tuple)
        elif choice == 5:
            check_out(connection_tuple)
        elif choice == 6:
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
home()