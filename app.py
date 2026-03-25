from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# ================= DATABASE =================
def get_db():
    conn = sqlite3.connect("church.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create table if not exists
def init_db():
    conn = get_db()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    conn.close()

init_db()

# ================= ROUTES =================

# HOME / MEMBERS PAGE
@app.route('/')
@app.route('/members')
def members():
    conn = get_db()
    members = conn.execute("SELECT * FROM members").fetchall()
    conn.close()
    return render_template("members.html", members=members)

# ADD MEMBER
@app.route('/add_member', methods=['POST'])
def add_member():
    data = request.form

    conn = get_db()
    conn.execute('''
    INSERT INTO members (
        member_id, names, id_number, phone, birthdate, gender,
        marital_status, parent_names,
        country, province, district, sector, cell, village,
        role, baptized, baptism_date, itsinda, status, reason
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('member_id'),
        data.get('names'),
        data.get('id_number'),
        data.get('phone'),
        data.get('birthdate'),
        data.get('gender'),
        data.get('marital_status'),
        data.get('parent_names'),

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
    conn.close()

    return redirect(url_for('members'))

# VIEW MEMBER (FULL DETAILS)
@app.route('/view_member/<int:id>')
def view_member(id):
    conn = get_db()
    member = conn.execute("SELECT * FROM members WHERE id = ?", (id,)).fetchone()
    conn.close()
    return render_template("view_member.html", member=member)

# DELETE MEMBER
@app.route('/delete_member/<int:id>')
def delete_member(id):
    conn = get_db()
    conn.execute("DELETE FROM members WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('members'))

# EDIT MEMBER PAGE
@app.route('/edit_member/<int:id>')
def edit_member(id):
    conn = get_db()
    member = conn.execute("SELECT * FROM members WHERE id = ?", (id,)).fetchone()
    conn.close()
    return render_template("edit_member.html", member=member)

# UPDATE MEMBER
@app.route('/update_member/<int:id>', methods=['POST'])
def update_member(id):
    data = request.form

    conn = get_db()
    conn.execute('''
    UPDATE members SET
        member_id=?,
        names=?,
        id_number=?,
        phone=?,
        birthdate=?,
        gender=?,
        marital_status=?,
        parent_names=?,

        country=?,
        province=?,
        district=?,
        sector=?,
        cell=?,
        village=?,

        role=?,
        baptized=?,
        baptism_date=?,
        itsinda=?,
        status=?,
        reason=?
    WHERE id=?
    ''', (
        data.get('member_id'),
        data.get('names'),
        data.get('id_number'),
        data.get('phone'),
        data.get('birthdate'),
        data.get('gender'),
        data.get('marital_status'),
        data.get('parent_names'),

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
        data.get('reason'),
        id
    ))

    conn.commit()
    conn.close()

    return redirect(url_for('members'))

# ================= RUN =================
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)