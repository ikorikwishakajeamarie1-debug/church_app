import os
from flask import Flask, render_template, request, redirect
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# ================= DATABASE CONNECTION =================
def get_db():
    database_url = os.environ.get("DATABASE_URL")

    # Render (production)
    if database_url:
        return psycopg2.connect(database_url)

    # Local development
    return psycopg2.connect(
        host="localhost",
        database="your_db_name",   # <-- CHANGE THIS
        user="postgres",           # <-- CHANGE THIS
        password="your_password"   # <-- CHANGE THIS
    )


# ================= INIT DATABASE =================
def init_db():
    conn = get_db()
    cur = conn.cursor()

    # MEMBERS TABLE (DO NOT DROP EXISTING DATA)
    cur.execute('''
    CREATE TABLE IF NOT EXISTS members (
        id SERIAL PRIMARY KEY,
        names TEXT,
        id_number TEXT,
        phone TEXT,
        birthdate TEXT,
        gender TEXT,
        marital_status TEXT,
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

    # STAFF TABLE
    cur.execute('''
    CREATE TABLE IF NOT EXISTS staff (
        id SERIAL PRIMARY KEY,
        names TEXT,
        id_number TEXT,
        gender TEXT,
        phone TEXT,
        role TEXT,
        status TEXT
    )
    ''')

    conn.commit()
    cur.close()
    conn.close()


# ================= HOME =================
@app.route('/')
def home():
    return redirect('/members')


# ================= MEMBERS =================
@app.route('/members')
def members():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM members ORDER BY id DESC")
    members = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('members.html', members=members)


# ================= ADD MEMBER =================
@app.route('/add_member', methods=['POST'])
def add_member():
    data = request.form

    conn = get_db()
    cur = conn.cursor()

    cur.execute('''
    INSERT INTO members (
        names, id_number, phone, birthdate, gender, marital_status,
        country, province, district, sector, cell, village,
        role, baptized, baptism_date, itsinda, status, reason
    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    ''', (
        data.get('names'),
        data.get('id_number'),
        data.get('phone'),
        data.get('birthdate'),
        data.get('gender'),
        data.get('marital_status'),
        data.get('country'),
        data.get('province'),
        data.get('district'),
        data.get('sector'),
        data.get('cell'),
        data.get('village'),
        data.get('role'),
        data.get('baptized'),
        data.get('baptism_date'),
        data.get('itsinda'),
        data.get('status'),
        data.get('reason')
    ))

    conn.commit()
    cur.close()
    conn.close()

    return redirect('/members')


# ================= VIEW MEMBER =================
@app.route('/view_member/<int:id>')
def view_member(id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM members WHERE id=%s", (id,))
    member = cur.fetchone()

    cur.close()
    conn.close()

    return render_template('view_member.html', member=member)


# ================= STAFF =================
@app.route('/staff')
def staff():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM staff ORDER BY id DESC")
    staff = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('staff.html', staff=staff)


# ================= ADD STAFF =================
@app.route('/add_staff', methods=['POST'])
def add_staff():
    data = request.form

    conn = get_db()
    cur = conn.cursor()

    cur.execute('''
    INSERT INTO staff (names, id_number, gender, phone, role, status)
    VALUES (%s,%s,%s,%s,%s,%s)
    ''', (
        data.get('names'),
        data.get('id_number'),
        data.get('gender'),
        data.get('phone'),
        data.get('role'),
        data.get('status')
    ))

    conn.commit()
    cur.close()
    conn.close()

    return redirect('/staff')


# ================= START APP =================
if __name__ == "__main__":
    init_db()   # ✅ creates tables if not exist
    app.run(debug=True)