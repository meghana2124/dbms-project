import mysql.connector
from tkinter import messagebox

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Sharsql@2025',
    'port': '3306',
    'database': 'student_skill_portfolio'
}

def create_db_connection():
    """Establishes a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to connect to MySQL: {err}")
        return None