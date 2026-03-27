from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

# ---------------- Database Connection ----------------
def get_db_connection():
    return psycopg2.connect(
        "postgresql://churchuser:RUMwAqWwKbyDikmWMwa4KTHyxU9bHRhN@dpg-d718i91r0fns73cd00ag-a.frankfurt-postgres.render.com:5432/churchdb_dbli"
    )

# ---------------- Home / Dashboard ----------------
@app.route("/")
def dashboard():
    return render_template("dashboard.html")

# ---------------- Members Page ----------------
@app.route("/members")
def members():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, first_name, last_name, id_number, date_of_birth, gender, phone, marital_status,
               country, province, district, sector, cell, village,
               role, baptized, baptism_date, itsinda, status, inactive_reason
        FROM members
        ORDER BY id DESC
    """)
    members_data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("members.html", members=members_data)

# ---------------- Add Member Page ----------------
@app.route("/add_member", methods=["GET", "POST"])
def add_member():
    if request.method == "POST":
        # Personal Identification
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        id_number = request.form.get("id_number")
        date_of_birth = request.form.get("date_of_birth")
        gender = request.form.get("gender")
        phone = request.form.get("phone")
        marital_status = request.form.get("marital_status")

        # Location Details
        country = request.form.get("country")
        province = request.form.get("province")
        district = request.form.get("district")
        sector = request.form.get("sector")
        cell = request.form.get("cell")
        village = request.form.get("village")

        # Church Responsibilities
        role = request.form.get("role")
        baptized = request.form.get("baptized")
        baptism_date = request.form.get("baptism_date") if baptized == "Yes" else None
        itsinda = request.form.get("itsinda")
        status = request.form.get("status")
        inactive_reason = request.form.get("inactive_reason") if status == "Inactive" else None

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO members
                (first_name, last_name, id_number, date_of_birth, gender, phone, marital_status,
                 country, province, district, sector, cell, village,
                 role, baptized, baptism_date, itsinda, status, inactive_reason)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (first_name, last_name, id_number, date_of_birth, gender, phone, marital_status,
                  country, province, district, sector, cell, village,
                  role, baptized, baptism_date, itsinda, status, inactive_reason))
            conn.commit()
            cur.close()
            conn.close()
            return redirect("/members")
        except Exception as e:
            return f"❌ Error inserting member: {e}"

    # GET request: show the Add Member form
    return render_template("add_member.html")
    
# ---------------- Run Flask ----------------
if __name__ == "__main__":
    app.run(debug=True)