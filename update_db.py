import sqlite3

conn = sqlite3.connect('church.db')
cur = conn.cursor()

columns = [
    ("id_number", "TEXT"),
    ("birthdate", "TEXT"),
    ("phone", "TEXT"),
    ("marital_status", "TEXT"),
    ("parent_name", "TEXT"),
    ("country", "TEXT"),
    ("province", "TEXT"),
    ("district", "TEXT"),
    ("sector", "TEXT"),
    ("cell", "TEXT"),
    ("village", "TEXT"),
    ("baptized", "TEXT"),
    ("itsinda", "TEXT"),
    ("photo", "TEXT")
]

for col, col_type in columns:
    try:
        cur.execute(f"ALTER TABLE members ADD COLUMN {col} {col_type}")
    except:
        pass

conn.commit()
conn.close()

print("Database updated successfully")