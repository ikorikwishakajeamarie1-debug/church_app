import os
from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# ================= DATABASE CONNECTION =================
def get_db():
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    return conn

# ================= INIT DATABASE =================
def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS members (
        id SERIAL PRIMARY KEY,
        member_id INTEGER,
        names TEXT,
        id_number TEXT,
        phone TEXT,
        birthdate TEXT,
        gender TEXT,
        marital_status TEXT,
        parent_names TEXT,
        country TEXT,
        province TEXT,
        district TEXT,
        sector TEXT,
        cell TEXT,
        village TEXT,
        role TEXT,
        baptized TEXT,
        baptism_date TEXT,
        itsinda TEXT,
        status TEXT,
        reason TEXT
    )
    ''')

    conn.commit()
    cur.close()
    conn.close()

# Run init once
init_db()

# ================= HELPER =================
def val(data, key, default=""):
    return data.get(key) or default

# ================= ROUTES =================

@app.route('/')
@app.route('/members')
def members():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM members ORDER BY id DESC")
    members = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("members.html", members=members)

# ================= ADD MEMBER =================
@app.route('/add_member', methods=['POST'])
def add_member():
    data = request.form

    conn = get_db()
    cur = conn.cursor()

    cur.execute('''
    INSERT INTO members (
        member_id, names, id_number, phone, birthdate, gender,
        marital_status, parent_names,
        country, province, district, sector, cell, village,
        role, baptized, baptism_date, itsinda, status, reason
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        val(data, "member_id", 0),
        val(data, "names", "Unknown"),
        val(data, "id_number"),
        val(data, "phone"),
        val(data, "birthdate"),
        val(data, "gender"),
        val(data, "marital_status"),
        val(data, "parent_names"),
        val(data, "country"),
        val(data, "province"),
        val(data, "district"),
        val(data, "sector"),
        val(data, "cell"),
        val(data, "village"),
        val(data, "role"),
        val(data, "baptized"),
        val(data, "baptism_date"),
        val(data, "itsinda"),
        val(data, "status", "Active"),
        val(data, "reason")
    ))

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('members'))

# ================= VIEW MEMBER =================
@app.route('/view_member/<int:id>')
def view_member(id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM members WHERE id = %s", (id,))
    member = cur.fetchone()

    cur.close()
    conn.close()

    return render_template("view_member.html", member=member)

# ================= DELETE MEMBER =================
@app.route('/delete_member/<int:id>')
def delete_member(id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM members WHERE id = %s", (id,))

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('members'))

# ================= TEST CONNECTION =================
@app.route('/test_db')
def test_db():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.close()
        conn.close()
        return "Database connection SUCCESS ✅"
    except Exception as e:
        return f"Database connection FAILED ❌: {e}"

# ================= RUN =================
if __name__ == '__main__':
    app.run(debug=True)