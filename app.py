from flask import Flask, render_template, request, redirect
import psycopg2
import os
import urllib.parse

app = Flask(__name__)

# ================= DATABASE CONNECTION =================
def get_db_connection():
    DATABASE_URL = os.environ.get("DATABASE_URL")
    if not DATABASE_URL:
        raise Exception("DATABASE_URL not set")

    result = urllib.parse.urlparse(DATABASE_URL)

    return psycopg2.connect(
        host=result.hostname,
        database=result.path[1:],
        user=result.username,
        password=result.password,
        port=result.port or 5432
    )

# ================= DASHBOARD =================
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# ================= MEMBERS =================
@app.route("/members")
def members():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM members ORDER BY id DESC")
    all_members = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("members.html", members=all_members)

# ================= ADD MEMBER =================
@app.route("/members/add", methods=["GET", "POST"])
def add_member():
    if request.method == "POST":
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO members (
                    names, id_number, birthdate, phone, gender, marital_status,
                    country, province, district, sector, cell, village,
                    role, baptized, baptism_date, itsinda, status, reason
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                request.form.get("names"),
                request.form.get("id_number"),
                request.form.get("birthdate"),
                request.form.get("phone"),
                request.form.get("gender"),
                request.form.get("marital_status"),
                request.form.get("country"),
                request.form.get("province"),
                request.form.get("district"),
                request.form.get("sector"),
                request.form.get("cell"),
                request.form.get("village"),
                request.form.get("role"),
                request.form.get("baptized"),
                request.form.get("baptism_date"),
                request.form.get("itsinda"),
                request.form.get("status"),
                request.form.get("reason")
            ))

            conn.commit()
            cur.close()
            conn.close()

            return redirect("/members")

        except Exception as e:
            print("Error inserting member:", e)
            return "❌ Error saving member"

    return render_template("add_member.html")

# ================= DELETE =================
@app.route('/delete_member/<int:id>')
def delete_member(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM members WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/members')

# ================= EDIT =================
@app.route('/edit_member/<int:id>')
def edit_member(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM members WHERE id=%s", (id,))
    member = cur.fetchone()
    cur.close()
    conn.close()

    return render_template('edit_member.html', member=member)

# ================= UPDATE =================
@app.route('/update_member/<int:id>', methods=['POST'])
def update_member(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE members SET
                names=%s, id_number=%s, birthdate=%s, phone=%s,
                gender=%s, marital_status=%s,
                country=%s, province=%s, district=%s,
                sector=%s, cell=%s, village=%s,
                role=%s, baptized=%s, baptism_date=%s,
                itsinda=%s, status=%s, reason=%s
            WHERE id=%s
        """, (
            request.form.get("names"),
            request.form.get("id_number"),
            request.form.get("birthdate"),
            request.form.get("phone"),
            request.form.get("gender"),
            request.form.get("marital_status"),
            request.form.get("country"),
            request.form.get("province"),
            request.form.get("district"),
            request.form.get("sector"),
            request.form.get("cell"),
            request.form.get("village"),
            request.form.get("role"),
            request.form.get("baptized"),
            request.form.get("baptism_date"),
            request.form.get("itsinda"),
            request.form.get("status"),
            request.form.get("reason"),
            id
        ))

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print("Error updating member:", e)
        return "❌ Error updating member"

    return redirect('/members')

# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)