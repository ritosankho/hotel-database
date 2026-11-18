from utils import *

# Checks the administrator password.
def admin_login():
    password = input("Enter admin password: ")
    creds = get_credentials()
    if password == creds["admin_passwd"]:
        print("Admin login successful.")
        return True
    else:
        print("Invalid admin password.")
        return False

# Authenticates a receptionist with employee details.
def receptionist_login(connection_tuple):
    cursor = connection_tuple[1]
    
    while True:
            
            e_id = input("Enter your employee ID:")
            name = input("Enter your name: ")
            password = input("Enter your password: ")
            try_cursor_execute(cursor, "select * from employees where e_id = %s", (e_id,))
            details = cursor.fetchone()
            print(details)
            if not details:
                print("Employee ID is invalid")
                continue
            if details[1] != name:
                print("Name is wrong")
                continue
            if details[2] != password:
                print("Wrong password")
                continue
            return True



    
# Registers a customer or employee.
def register(connection_tuple,person = "customer"):
    if person.lower() == "customer":
        generated_id = generate_id(connection_tuple, "customer")
        table = "customer"
    elif person.lower() == "employee":
        generated_id = generate_id(connection_tuple, "employee")
        table = "employees"
    while True:
        name = input("Enter name: ")
        password = input("Create a strong password within 20 characters: ")
        if len(password) > 20:
            print("Password too long")
            continue
        proceed = input("Are the particulars entered above correct? (Y/N)")
        if proceed.lower() == "y":
            break
        else:
            continue
    
    connection = connection_tuple[0]
    cursor = connection_tuple[1]
    try_cursor_execute(cursor, f"insert into {table} values(%s,%s,%s)",(generated_id, name, password))
    try:
        connection.commit()
    except error as e:
        print(e)
        return
    print(f"Registered successfully. Your customer ID is {generated_id}")


# Logs in or registers a customer.
def customer_login(connection_tuple):
    cursor = connection_tuple[1]
    
    print("1. Login")
    print("2. Register")
    choice = int_input("Enter yout choice: ")
    if choice == 2:
        register(connection_tuple)
        return True
    elif choice ==1:
        while True:
            
            c_id = input("Enter your customer ID:")
            username = input("Enter your name: ")
            password = input("Enter your password: ")
            try_cursor_execute(cursor, "select * from customer where c_id = %s", (c_id,))
            details = cursor.fetchone()
            if not details:
                print("Customer ID is invalid")
                continue
            if details[1] != username:
                print("The Name is invalid")
                continue
            if details[2] != password:
                print("Wrong password")
                continue
            return True
    
    
# Deletes an employee selected by the administrator.
def delete_employee(connection_tuple):
    cursor = connection_tuple[1]
    employee_id = input("Enter the employees ID to delete, press 0 to exit: ")
    if employee_id != "0":
        try_cursor_execute(cursor, "select * from employee where e_id=%s", (employee_id,))
        employee = cursor.fetchone()
        if not employee:
            print(f"Employee ID {employee_id} does not exist")
        else:
            try_cursor_execute(cursor, "delete from employee where e_id=%s", (employee_id,))
            connection_tuple[0].commit()
            print(f"Deleted employee {employee_id}")
    


# Prompts for a role and verifies the corresponding login.
def login_prompt(connection_tuple):
    print("Welcome to the Hotel Management System")
    print("Please select your role:")
    print("1. Admin")
    print("2. Receptionist")
    print("3. Customer")
    
    while True:
        choice = int_input("Enter your choice (1-3): ")
        if choice == 1:
            if admin_login():
                return "admin"
        elif choice == 2:
            if receptionist_login(connection_tuple):
                return "receptionist"
        elif choice == 3:
            if customer_login(connection_tuple):
                return "customer"
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")