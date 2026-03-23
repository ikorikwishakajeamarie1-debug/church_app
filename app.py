from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "church.db"
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def update_table():
    conn = get_db_connection()

    try:
        conn.execute("ALTER TABLE members ADD COLUMN id_number TEXT")
    except:
        pass

    conn.commit()
    conn.close()

update_table()

# ================= ROUTES =================

@app.route('/add', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        conn = get_db_connection()

        conn.execute("""
            INSERT INTO members (
                name, id_number, birthdate, phone, gender, marital_status, parents,
                country, province, district, sector, cell, village,
                role, baptized, itsinda
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            request.form['name'],
            request.form['id_number'],
            request.form['birthdate'],
            request.form['phone'],
            request.form['gender'],
            request.form['marital_status'],
            request.form['parents'],
            request.form['country'],
            request.form['province'],
            request.form['district'],
            request.form['sector'],
            request.form['cell'],
            request.form['village'],
            request.form['role'],
            request.form['baptized'],
            request.form['itsinda']
        ))

        conn.commit()
        conn.close()

        return redirect(url_for('members'))

    return render_template('add_member.html')
@app.route('/')
def home():
    return redirect('/members')
@app.route('/')
def home():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/members')
def members():
    conn = get_db_connection()
    members = conn.execute("SELECT * FROM members").fetchall()
    conn.close()
    return render_template('members.html', members=members)

@app.route('/view/<int:id>')
def view_member(id):
    conn = get_db_connection()
    member = conn.execute("SELECT * FROM members WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template('view_member.html', member=member)
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_member(id):
    # your edit code here
    pass
if __name__ == '__main__':
    app.run(debug=True)