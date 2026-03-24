from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# -----------------------------
# DATABASE PATH (IMPORTANT FOR RENDER)
# -----------------------------
DB_PATH = '/tmp/church.db'


# -----------------------------
# DATABASE CONNECTION
# -----------------------------
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# INITIALIZE DATABASE
# -----------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            id_number TEXT,
            birthdate TEXT,
            phone TEXT,
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
            itsinda TEXT
        )
    ''')
    conn.close()

init_db()


# -----------------------------
# HOME / DASHBOARD
# -----------------------------
@app.route('/')
def home():
    conn = get_db_connection()
    members = conn.execute('SELECT * FROM members').fetchall()
    conn.close()
    return render_template('dashboard.html', members=members)


# -----------------------------
# MEMBERS LIST
# -----------------------------
@app.route('/members')
def members():
    conn = get_db_connection()
    members = conn.execute('SELECT * FROM members').fetchall()
    conn.close()
    return render_template('members.html', members=members)


# -----------------------------
# ADD MEMBER
# -----------------------------
@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        name = request.form.get('name')
        id_number = request.form.get('id_number')
        birthdate = request.form.get('birthdate')
        phone = request.form.get('phone')
        gender = request.form.get('gender')
        marital_status = request.form.get('marital_status')
        country = request.form.get('country')
        province = request.form.get('province')
        district = request.form.get('district')
        sector = request.form.get('sector')
        cell = request.form.get('cell')
        village = request.form.get('village')
        role = request.form.get('role')
        baptized = request.form.get('baptized')
        itsinda = request.form.get('itsinda')

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO members (
                name, id_number, birthdate, phone, gender, marital_status,
                country, province, district, sector, cell, village,
                role, baptized, itsinda
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            name, id_number, birthdate, phone, gender, marital_status,
            country, province, district, sector, cell, village,
            role, baptized, itsinda
        ))
        conn.commit()
        conn.close()

        return redirect(url_for('members'))

    return render_template('add_member.html')


# -----------------------------
# VIEW MEMBER
# -----------------------------
@app.route('/view/<int:id>')
def view_member(id):
    conn = get_db_connection()
    member = conn.execute('SELECT * FROM members WHERE id=?', (id,)).fetchone()
    conn.close()
    return render_template('view_member.html', member=member)


# -----------------------------
# EDIT MEMBER
# -----------------------------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_member(id):
    conn = get_db_connection()
    member = conn.execute('SELECT * FROM members WHERE id=?', (id,)).fetchone()

    if request.method == 'POST':
        conn.execute('''
            UPDATE members SET
                name=?, id_number=?, birthdate=?, phone=?, gender=?, marital_status=?,
                country=?, province=?, district=?, sector=?, cell=?, village=?,
                role=?, baptized=?, itsinda=?
            WHERE id=?
        ''', (
            request.form.get('name'),
            request.form.get('id_number'),
            request.form.get('birthdate'),
            request.form.get('phone'),
            request.form.get('gender'),
            request.form.get('marital_status'),
            request.form.get('country'),
            request.form.get('province'),
            request.form.get('district'),
            request.form.get('sector'),
            request.form.get('cell'),
            request.form.get('village'),
            request.form.get('role'),
            request.form.get('baptized'),
            request.form.get('itsinda'),
            id
        ))

        conn.commit()
        conn.close()
        return redirect(url_for('members'))

    conn.close()
    return render_template('edit_member.html', member=member)


# -----------------------------
# DELETE MEMBER
# -----------------------------
@app.route('/delete/<int:id>')
def delete_member(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM members WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('members'))


# -----------------------------
# RUN APP (RENDER READY)
# -----------------------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)