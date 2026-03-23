import sqlite3

conn = sqlite3.connect('church.db')
cur = conn.cursor()

# Add gender column
try:
    cur.execute("ALTER TABLE members ADD COLUMN gender TEXT")
    print("Gender column added successfully")
except Exception as e:
    print("Column may already exist:", e)

conn.commit()
conn.close()