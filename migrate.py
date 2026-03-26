# migrate.py
import sqlite3
import os

# ===== CONNECT SQLITE =====
try:
    sqlite_conn = sqlite3.connect("church.db")  # assumes church.db is in the same folder
    sqlite_cur = sqlite_conn.cursor()
    print("✅ Connected to SQLite database 'church.db'")
except Exception as e:
    print("❌ Failed to connect to SQLite:", e)
    exit()

# ===== CONNECT POSTGRESQL (OPTIONAL) =====
DATABASE_URL = os.environ.get("DATABASE_URL")
pg_conn = None
pg_cur = None

if DATABASE_URL:
    try:
        import psycopg2
        pg_conn = psycopg2.connect(DATABASE_URL)
        pg_cur = pg_conn.cursor()
        print("✅ Connected to PostgreSQL database")
    except Exception as e:
        print("❌ Failed to connect to PostgreSQL:", e)
        pg_conn = None
        pg_cur = None
else:
    print("⚠️ DATABASE_URL not found. Skipping PostgreSQL migration.")

# ===== FETCH DATA FROM SQLITE =====
try:
    sqlite_cur.execute("SELECT * FROM members")
    rows = sqlite_cur.fetchall()
    print(f"ℹ️ Found {len(rows)} records in SQLite")
except Exception as e:
    print("❌ Failed to fetch data from SQLite:", e)
    sqlite_conn.close()
    if pg_conn: pg_conn.close()
    exit()

# ===== INSERT INTO POSTGRESQL IF AVAILABLE =====
if pg_cur:
    inserted = 0
    for row in rows:
        try:
            pg_cur.execute("""
                INSERT INTO members (
                    names, id_number, phone, birthdate, gender, marital_status,
                    country, province, district, sector, cell, village,
                    role, baptized, baptism_date, itsinda, status, reason
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                row[1], row[2], row[3], row[4], row[5], row[6],
                row[7], row[8], row[9], row[10], row[11], row[12],
                row[13], row[14], row[15], row[16], row[17], row[18]
            ))
            inserted += 1
        except Exception as e:
            print("❌ Error inserting row into PostgreSQL:", e)
    pg_conn.commit()
    print(f"✅ Migration to PostgreSQL completed. {inserted} records inserted.")
else:
    print("ℹ️ PostgreSQL migration skipped. Only SQLite data read.")

# ===== CLOSE CONNECTIONS =====
sqlite_conn.close()
if pg_conn:
    pg_conn.close()
print("✅ All database connections closed.")