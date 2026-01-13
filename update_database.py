import sqlite3

conn = sqlite3.connect("users.db")
c = conn.cursor()

# Add last_diagnosis column if it doesn't already exist
try:
    c.execute("ALTER TABLE profiles ADD COLUMN last_diagnosis TEXT")
    print("Column 'last_diagnosis' added.")
except sqlite3.OperationalError:
    print("Column 'last_diagnosis' already exists.")

conn.commit()
conn.close()
