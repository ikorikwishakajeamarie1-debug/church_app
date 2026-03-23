import sqlite3

conn = sqlite3.connect('church.db')
cursor = conn.cursor()

# Create table with all required columns
cursor.execute("""
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    id_number TEXT,
    birthdate TEXT,
    country TEXT,
    province TEXT,
    district TEXT,
    sector TEXT,
    cell TEXT,
    village TEXT,
    gender TEXT,
    parents_name TEXT,
    marital_status TEXT,
    role TEXT,
    baptized TEXT,
    itsinda TEXT,
    phone TEXT
)
""")

conn.commit()
conn.close()

print("Database initialized successfully!")