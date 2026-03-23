import sqlite3

conn = sqlite3.connect('church.db')
cursor = conn.cursor()

# List of columns to ensure exist
columns = [
    ("parent_name", "TEXT"),
    ("country", "TEXT"),
    ("province", "TEXT"),
    ("district", "TEXT"),
    ("sector", "TEXT"),
    ("cell", "TEXT"),
    ("village", "TEXT"),
    ("baptized", "TEXT"),
    ("itsinda", "TEXT"),
    ("role", "TEXT"),
    ("phone", "TEXT"),
    ("marital_status", "TEXT")
]

# Get existing columns
cursor.execute("PRAGMA table_info(members)")
existing_columns = [col[1] for col in cursor.fetchall()]

# Add missing columns only
for column_name, column_type in columns:
    if column_name not in existing_columns:
        cursor.execute(f"ALTER TABLE members ADD COLUMN {column_name} {column_type}")
        print(f"Added column: {column_name}")
    else:
        print(f"Column already exists: {column_name}")

conn.commit()
conn.close()

print("✅ All missing columns added successfully!")