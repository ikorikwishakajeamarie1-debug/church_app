import sqlite3

conn = sqlite3.connect('church.db')
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE members ADD COLUMN birthdate TEXT")
    print("birthdate column added successfully ✅")
except Exception as e:
    print("Column may already exist or error occurred:", e)

conn.commit()
conn.close()