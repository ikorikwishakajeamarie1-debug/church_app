import sqlite3

conn = sqlite3.connect('church.db')
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE members ADD COLUMN member_id INTEGER")
    print("member_id column added successfully ✅")
except Exception as e:
    print("Column may already exist or error occurred:", e)

conn.commit()
conn.close()