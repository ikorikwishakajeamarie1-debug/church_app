import psycopg2
import csv

conn = psycopg2.connect(
    "postgresql://churchuser:RUMwAqWwKbyDikmWMwa4KTHyxU9bHRhN@dpg-d718i91r0fns73cd00ag-a.frankfurt-postgres.render.com/churchdb_dbli"
)

cur = conn.cursor()
cur.execute("SELECT * FROM members")
rows = cur.fetchall()

# Save to CSV
with open("members_backup.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([desc[0] for desc in cur.description])  # column names
    writer.writerows(rows)

cur.close()
conn.close()

print("✅ Backup saved as members_backup.csv")