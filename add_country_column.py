import sqlite3

conn = sqlite3.connect('church.db')
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE members ADD COLUMN country TEXT")
    print("country column added successfully ✅")
except Exception as e:
    print("Column may already exist or error occurred:", e)

conn.commit()
conn.close()