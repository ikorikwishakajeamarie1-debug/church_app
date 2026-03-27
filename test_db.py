import psycopg2

conn = psycopg2.connect(
    "postgresql://churchuser:RUMwAqWwKbyDikmWMwa4KTHyxU9bHRhN@dpg-d718i91r0fns73cd00ag-a.frankfurt-postgres.render.com:5432/churchdb_dbli"
)

cur = conn.cursor()

cur.execute("SELECT * FROM members;")
rows = cur.fetchall()

print("Records:", len(rows))

for row in rows:
    print(row)

cur.close()
conn.close()