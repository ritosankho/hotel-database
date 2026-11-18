from app import *
from login import *

# Displays the admin options.
def print_admin_menu():
    print("Hotel Management System - Admin Dashboard")
    print("===============================================")
    print("Main Menu:")
    print("0. Exit")
    print("1. Show Price of a Room")
    print("2. Update Price of a Room")
    print("3. Display Rooms by Floor")
    print("4. Show Booking Details")
    print("5. Show All Bookings")
    print("6. Register a new Employee")
    print("7. Delete an Employee from the Database")

# Displays the receptionist options.
def print_receptionist_menu():
    print("Hotel Management System - Receptionist Dashboard")
    print("===============================================")
    print("Main Menu:")
    print("0. Exit")
    print("1. Show Price of a Room")
    print("3. Display Rooms by Floor")
    print("4. Show Booking Details")
    print("5. Show All Bookings")
    
# Displays the customer options.
def print_customer_menu():
    print("Hotel Management System - Customer Dashboard")
    print("===============================================")
    print("Main Menu:")
    print("0. Exit")
    print("1. Show Price of a Room")
    print("3. Display Rooms by Floor")
    print("4. Show Available Rooms")
    print("5. Book a room")
    print("6. Cancel a booking")





# Connects to the database and routes users to role-specific menus.
def home():
    try:
        connection_tuple = connect()
    except Exception as e:
        print("Failed to connect to database.")
        print(e)
        return

    role = login_prompt(connection_tuple)

    if role == "admin":
        while True:
            print_admin_menu()
            choice = int_input("Enter your choice (0-7): ")
            if choice == 0:
                print("Exiting the program.")
                break
            elif choice == 1:
                show_price(connection_tuple)
            elif choice == 2:
                update_price(connection_tuple)
            elif choice == 3:
                display_floors(connection_tuple)
            elif choice == 4:
                show_booking_details(connection_tuple)
            elif choice == 5:
                show_all_bookings(connection_tuple)
            elif choice == 6:
                register(connection_tuple, "employee")
            elif choice == 7:
                delete_employee(connection_tuple)
            else:
                print("Invalid choice. Please enter a number between 0 and 7.")

    elif role == "receptionist":
        while True:
            print_receptionist_menu()
            choice = int_input("Enter your choice (0-5): ")
            if choice == 0:
                print("Exiting the program.")
                break
            elif choice == 1:
                show_price(connection_tuple)
            elif choice == 3:
                display_floors(connection_tuple)
            elif choice == 4:
                show_booking_details(connection_tuple)
            elif choice == 5:
                show_all_bookings(connection_tuple)
            else:
                print("Invalid choice. Please enter 0, 1, 3, 4, or 5.")

    elif role == "customer":
        while True:
            print_customer_menu()
            choice = int_input("Enter your choice (0-6): ")
            if choice == 0:
                print("Exiting the program.")
                break
            elif choice == 1:
                show_price(connection_tuple)
            elif choice == 3:
                display_floors(connection_tuple)
            elif choice == 4:
                display_vaccant_rooms(connection_tuple)
            elif choice == 5:
                book(connection_tuple)
            elif choice == 6:
                cancel_booking(connection_tuple)
            else:
                print("Invalid choice. Please enter a number between 0 and 6.")


home()