# db.py
import sqlite3
from werkzeug.security import generate_password_hash

DATABASE = 'hospital.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    conn = get_db()
    cursor = conn.cursor()

    tables = {
        "admin": '''CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL)''',

        "doctors": '''CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT NOT NULL,
            gender TEXT NOT NULL,
            experience INTEGER NOT NULL,
            contact TEXT,
            available_slots INTEGER NOT NULL)''',

       "patients": '''CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL,
    contact TEXT,
    username TEXT UNIQUE NOT NULL)''',

        "lab_admins": '''CREATE TABLE IF NOT EXISTS lab_admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT NOT NULL,
            phone TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL)''',

        "doctor_logins": '''CREATE TABLE IF NOT EXISTS doctor_logins (
            doctor_id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            FOREIGN KEY (doctor_id) REFERENCES doctors(id))''',

        "patient_logins": '''CREATE TABLE IF NOT EXISTS patient_logins (
            patient_id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients(id))''',

        "labadmin_logins": '''CREATE TABLE IF NOT EXISTS labadmin_logins (
            labadmin_id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            FOREIGN KEY (labadmin_id) REFERENCES lab_admins(id))''',

       "medical_records": '''CREATE TABLE IF NOT EXISTS medical_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            scan_and_report TEXT,
            normal_report TEXT,
            upload_date DATE,
            FOREIGN KEY (username) REFERENCES patients(username))''',
            "doctor_slots": '''CREATE TABLE IF NOT EXISTS doctor_slots (
            slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_username TEXT NOT NULL,
            slot_datetime DATETIME NOT NULL,
            is_booked INTEGER DEFAULT 0,
            FOREIGN KEY (doctor_username) REFERENCES doctors(username))''',

        "appointments": '''CREATE TABLE IF NOT EXISTS appointments (
            appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot_id INTEGER NOT NULL,
            doctor_username TEXT NOT NULL,
            patient_username TEXT NOT NULL,
            FOREIGN KEY (slot_id) REFERENCES doctor_slots(slot_id),
            FOREIGN KEY (doctor_username) REFERENCES doctors(username),
            FOREIGN KEY (patient_username) REFERENCES patients(username))''',





        }

    # Create tables in proper order
    for table_name, create_sql in tables.items():
        cursor.execute(create_sql)

    # Insert default admin if not present
    cursor.execute("SELECT COUNT(*) as count FROM admin")
    if cursor.fetchone()["count"] == 0:
        default_admin = ('admin', generate_password_hash('admin123'))
        cursor.execute("INSERT INTO admin (username, password) VALUES (?, ?)", default_admin)

    conn.commit()
    conn.close()
