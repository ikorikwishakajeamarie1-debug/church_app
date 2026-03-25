from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

# ==============================
# DATABASE CONNECTION
# ==============================
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=5432
    )
    return conn


# ==============================
# HOME / DASHBOARD
# ==============================
@app.route('/')
def dashboard():
    return render_template('dashboard.html')


# ==============================
# MEMBERS
# ==============================
@app.route('/members')
def members():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM members")
    members = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('members.html', members=members)


# ==============================
# STAFF - VIEW
# ==============================
@app.route('/staff')
def staff():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM staff")
    staff = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('staff.html', staff=staff)


# ==============================
# STAFF - ADD FORM
# ==============================
@app.route('/staff/add')
def add_staff():
    return render_template('add_staff.html')


# ==============================
# STAFF - SAVE
# ==============================
@app.route('/save_staff', methods=['POST'])
def save_staff():
    name = request.form.get('name')
    id_number = request.form.get('id_number')
    gender = request.form.get('gender')
    role = request.form.get('role')
    phone = request.form.get('phone')
    status = request.form.get('status')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO staff (name, id_number, gender, role, phone, status)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (name, id_number, gender, role, phone, status))

    conn.commit()
    cur.close()
    conn.close()

    return redirect('/staff')


# ==============================
# STAFF - DELETE
# ==============================
@app.route('/delete_staff/<int:id>')
def delete_staff(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM staff WHERE id = %s", (id,))

    conn.commit()
    cur.close()
    conn.close()

    return redirect('/staff')


# ==============================
# STAFF - EDIT FORM
# ==============================
@app.route('/edit_staff/<int:id>')
def edit_staff(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM staff WHERE id = %s", (id,))
    staff = cur.fetchone()

    cur.close()
    conn.close()

    return render_template('edit_staff.html', staff=staff)


# ==============================
# STAFF - UPDATE
# ==============================
@app.route('/update_staff/<int:id>', methods=['POST'])
def update_staff(id):
    name = request.form.get('name')
    id_number = request.form.get('id_number')
    gender = request.form.get('gender')
    role = request.form.get('role')
    phone = request.form.get('phone')
    status = request.form.get('status')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE staff
        SET name=%s, id_number=%s, gender=%s, role=%s, phone=%s, status=%s
        WHERE id=%s
    """, (name, id_number, gender, role, phone, status, id))

    conn.commit()
    cur.close()
    conn.close()

    return redirect('/staff')


# ==============================
# RUN APP
# ==============================
if __name__ == "__main__":
    app.run(debug=True)