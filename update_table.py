import psycopg2

conn = psycopg2.connect(
    "postgresql://churchuser:PASSWORD@FULL_HOST:5432/churchdb_dbli"
)
cur = conn.cursor()

# Add missing columns safely (only if they don't exist)
columns = [
    "first_name VARCHAR(100)",
    "last_name VARCHAR(100)",
    "id_number VARCHAR(50)",
    "date_of_birth DATE",
    "gender VARCHAR(10)",
    "phone VARCHAR(20)",
    "marital_status VARCHAR(20)",
    "country VARCHAR(50)",
    "province VARCHAR(50)",
    "district VARCHAR(50)",
    "sector VARCHAR(50)",
    "cell VARCHAR(50)",
    "village VARCHAR(50)",
    "role VARCHAR(50)",
    "baptized VARCHAR(5)",
    "baptism_date DATE",
    "itsinda VARCHAR(50)",
    "status VARCHAR(20)",
    "inactive_reason TEXT"
]

for col in columns:
    cur.execute(f"ALTER TABLE members ADD COLUMN IF NOT EXISTS {col};")

conn.commit()
cur.close()
conn.close()

print("✅ Table updated successfully")