from flask import Flask, render_template, request, redirect
import psycopg2
import os
import urllib.parse

app = Flask(__name__)

# ================= DATABASE CONNECTION =================
def get_db_connection():
    DATABASE_URL = os.environ.get("DATABASE_URL")
    if not DATABASE_URL:
        raise Exception("DATABASE_URL not set. Please set it to your church-db URL.")
    
    # Parse URL for psycopg2
    result = urllib.parse.urlparse(DATABASE_URL)
    username = result.username
    password = result.password
    database = result.path[1:]  # remove leading /
    hostname = result.hostname
    port = result.port or 5432
    
    conn = psycopg2.connect(
        host=hostname,
        database=database,
        user=username,
        password=password,
        port=port
    )
    return conn

# ================= DASHBOARD =================
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# ================= MEMBERS =================
@app.route('/members')
def members():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM members ORDER BY id ASC")
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
        request.form.get('name'),
        request.form.get('id_number'),
        request.form.get('birthdate'),
        request.form.get('phone'),
        request.form.get('gender'),
        request.form.get('marital_status'),
        request.form.get('parent_name'),
        request.form.get('country'),
        request.form.get('province'),
        request.form.get('district'),
        request.form.get('sector'),
        request.form.get('cell'),
        request.form.get('village'),
        request.form.get('role'),
        request.form.get('baptized'),
        request.form.get('baptized_date'),
        request.form.get('itsinda'),
        request.form.get('status'),
        request.form.get('reason')
    )

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO members (
                names, id_number, birthdate, phone, gender, marital_status,
                parent_name, country, province, district, sector, cell, village,
                role, baptized, baptism_date, itsinda, status, reason
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, data)
        conn.commit()
        cur.close()
        conn.close()
        return redirect('/members')
    except Exception as e:
        print("Error inserting member:", e)
        return "❌ Internal Server Error — check console/logs"

# DELETE MEMBER
@app.route('/delete_member/<int:id>')
def delete_member(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM members WHERE id=%s", (id,))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("Error deleting member:", e)
    return redirect('/members')

# EDIT MEMBER
@app.route('/edit_member/<int:id>')
def edit_member(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM members WHERE id=%s", (id,))
    member = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('edit_member.html', member=member)

# UPDATE MEMBER
@app.route('/update_member/<int:id>', methods=['POST'])
def update_member(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE members SET
                names=%s, id_number=%s, birthdate=%s, phone=%s, gender=%s,
                marital_status=%s, parent_name=%s, country=%s, province=%s, district=%s,
                sector=%s, cell=%s, village=%s, role=%s, baptized=%s, baptism_date=%s,
                itsinda=%s, status=%s, reason=%s
            WHERE id=%s
        """, (
            request.form.get('name'),
            request.form.get('id_number'),
            request.form.get('birthdate'),
            request.form.get('phone'),
            request.form.get('gender'),
            request.form.get('marital_status'),
            request.form.get('parent_name'),
            request.form.get('country'),
            request.form.get('province'),
            request.form.get('district'),
            request.form.get('sector'),
            request.form.get('cell'),
            request.form.get('village'),
            request.form.get('role'),
            request.form.get('baptized'),
            request.form.get('baptized_date'),
            request.form.get('itsinda'),
            request.form.get('status'),
            request.form.get('reason'),
            id
        ))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("Error updating member:", e)
        return "❌ Internal Server Error — check console/logs"
    return redirect('/members')

if __name__ == "__main__":
    app.run(debug=True)