import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="postgres",   # connect to default DB
    user="postgres",
    password="Church123@"  # the one you just created
)

cur = conn.cursor()

# List all databases
cur.execute("SELECT datname FROM pg_database;")
dbs = cur.fetchall()

print("Databases:")
for db in dbs:
    print(db[0])

cur.close()
conn.close()