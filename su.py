import sqlite3
def drop_appointments_table():
    conn = sqlite3.connect('hospital.db')  # Replace with your actual DB name
    cursor = conn.cursor()
    try:
        cursor.execute("DROP TABLE IF EXISTS doctor_slots")
        conn.commit()
        print("✅ 'dotor_lofins' table dropped successfully.")
    except Exception as e:
        print("❌ Error dropping table:", e)
    finally:
        conn.close()
drop_appointments_table()