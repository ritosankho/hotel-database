# Hotel Database

A command-line hotel management system using Python, PyMySQL, and MySQL.

## Features

- Admin login and employee management
- Receptionist login and booking lookup
- Customer registration, login, room booking, and cancellation
- Room prices, floor listings, and availability

## Requirements

- Python 3
- MySQL
- `pymysql`
- `tabulate`
- `python-dotenv`

Install dependencies:

```bash
pip install pymysql tabulate python-dotenv
```

## Configuration

Create a `.env` file in the project directory:

```env
OPERATOR=your_database_user
DB_PASSWORD=your_database_password
ADMIN_PASSWORD=your_admin_password
HOST=localhost
DBNAME=hotel
```

Create MySQL tables for `rooms`, `bookings`, `customer`, and `employees` before running the application.

## Run

```bash
python main.py
```