from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

# DATABASE CONNECTION
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=5432
    )

# DASHBOARD
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# ================= MEMBERS =================

# VIEW MEMBERS
@app.route('/members')
def members():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM members")
    members = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('members.html', members=members)

# ADD MEMBER PAGE
@app.route('/members/add')
def add_member():
    return render_template('add_member.html')

# SAVE MEMBER
@app.route('/save_member', methods=['POST'])
def save_member():
    data = (
        request.form['name'],
        request.form['id_number'],
        request.form['birthdate'],
        request.form['phone'],
        request.form['gender'],
        request.form['marital_status'],
        request.form.get('parent_name'),
        request.form['district'],
        request.form['sector'],
        request.form['cell'],
        request.form['village'],
        request.form['role'],
        request.form['baptized'],
        request.form.get('baptized_date'),
        request.form['status'],
        request.form.get('reason')
    )

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO members 
    (name, id_number, birthdate, phone, gender, marital_status, parent_name,
     district, sector, cell, village, role, baptized, baptized_date, status, reason)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, data)

    conn.commit()
    cur.close()
    conn.close()

    return redirect('/members')


# DELETE
@app.route('/delete_member/<int:id>')
def delete_member(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM members WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/members')


# EDIT
@app.route('/edit_member/<int:id>')
def edit_member(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM members WHERE id=%s", (id,))
    member = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('edit_member.html', member=member)


# UPDATE
@app.route('/update_member/<int:id>', methods=['POST'])
def update_member(id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    UPDATE members SET
    name=%s, id_number=%s, phone=%s, gender=%s, status=%s
    WHERE id=%s
    """, (
        request.form['name'],
        request.form['id_number'],
        request.form['phone'],
        request.form['gender'],
        request.form['status'],
        id
    ))

    conn.commit()
    cur.close()
    conn.close()

    return redirect('/members')


if __name__ == "__main__":
    app.run(debug=True)