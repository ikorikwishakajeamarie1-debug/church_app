import sqlite3

conn = sqlite3.connect('church.db')
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE members ADD COLUMN id_number TEXT")
    print("id_number column added successfully ✅")
except Exception as e:
    print("Column may already exist or error occurred:", e)

conn.commit()
conn.close()