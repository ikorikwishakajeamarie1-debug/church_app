import sqlite3

conn = sqlite3.connect('church.db')
cursor = conn.cursor()

cursor.execute("ALTER TABLE members ADD COLUMN itsinda TEXT")

conn.commit()
conn.close()

print("Column 'itsinda' added successfully")