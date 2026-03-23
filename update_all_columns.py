import sqlite3

conn = sqlite3.connect('church.db')
cursor = conn.cursor()

columns = [
    ("id_number", "TEXT"),
    ("phone", "TEXT"),
    ("birthdate", "TEXT"),
    ("country", "TEXT"),
    ("province", "TEXT"),
    ("district", "TEXT"),
    ("sector", "TEXT"),
    ("cell", "TEXT"),
    ("village", "TEXT"),
    ("gender", "TEXT"),
    ("parents_name", "TEXT"),
    ("marital_status", "TEXT"),
    ("role", "TEXT"),
    ("baptized", "TEXT"),
    ("group_name", "TEXT")
]

for column_name, column_type in columns:
    try:
        cursor.execute(f"ALTER TABLE members ADD COLUMN {column_name} {column_type}")
        print(f"{column_name} added successfully ✅")
    except Exception as e:
        print(f"{column_name} already exists or error: {e}")

conn.commit()
conn.close()

print("Database update completed 🎉")