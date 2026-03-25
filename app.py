from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# ================= DATABASE =================
def get_db():
    conn = sqlite3.connect("church.db")
    conn.row_factory = sqlite3.Row
    return conn

# ================= INIT =================
def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT
        )
    ''')
    conn.commit()
    conn.close()

# ================= MIGRATION =================
def update_db():
    conn = get_db()
    cursor = conn.cursor()

    columns = [
        ("member_id", "INTEGER"),
        ("names", "TEXT"),
        ("id_number", "TEXT"),
        ("phone", "TEXT"),
        ("birthdate", "TEXT"),
        ("gender", "TEXT"),
        ("marital_status", "TEXT"),
        ("parent_names", "TEXT"),
        ("country", "TEXT"),
        ("province", "TEXT"),
        ("district", "TEXT"),
        ("sector", "TEXT"),
        ("cell", "TEXT"),
        ("village", "TEXT"),
        ("role", "TEXT"),
        ("baptized", "TEXT"),
        ("baptism_date", "TEXT"),
        ("itsinda", "TEXT"),
        ("status", "TEXT"),
        ("reason", "TEXT")
    ]

    for col, typ in columns:
        try:
            cursor.execute(f"ALTER TABLE members ADD COLUMN {col} {typ}")
        except:
            pass

    conn.commit()
    conn.close()

init_db()
update_db()

# ================= HELPER =================
def val(data, key, default=""):
    return data.get(key) or default

# ================= ROUTES =================

@app.route('/')
@app.route('/members')
def members():
    conn = get_db()
    members = conn.execute("SELECT * FROM members ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("members.html", members=members)

# ================= ADD MEMBER =================
@app.route('/add_member', methods=['POST'])
def add_member():
    data = request.form

    # Debug (optional)
    print("FORM DATA RECEIVED:", data)

    conn = get_db()
    conn.execute('''
    INSERT INTO members (
        member_id, names, id_number, phone, birthdate, gender,
        marital_status, parent_names,
        country, province, district, sector, cell, village,
        role, baptized, baptism_date, itsinda, status, reason
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
    conn.close()

    return redirect(url_for('members'))

# ================= VIEW =================
@app.route('/view_member/<int:id>')
def view_member(id):
    conn = get_db()
    member = conn.execute("SELECT * FROM members WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("view_member.html", member=member)

# ================= DELETE =================
@app.route('/delete_member/<int:id>')
def delete_member(id):
    conn = get_db()
    conn.execute("DELETE FROM members WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('members'))

# ================= RUN =================
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)