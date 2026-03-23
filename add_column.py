import sqlite3

print("Starting script...")

conn = sqlite3.connect('church.db')

cursor = conn.execute("PRAGMA table_info(members)")
columns = [col[1] for col in cursor.fetchall()]

print("Existing columns:", columns)

if 'decision' not in columns:
    conn.execute("ALTER TABLE members ADD COLUMN decision TEXT")
    print("✅ Column 'decision' added successfully.")
else:
    print("ℹ️ Column already exists.")

conn.commit()
conn.close()

print("Done.")