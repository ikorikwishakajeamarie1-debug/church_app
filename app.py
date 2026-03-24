import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ================= DATABASE CONFIG =================
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///local.db")

# Fix for Render PostgreSQL URL
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ================= MODEL =================
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Personal Identification
    full_name = db.Column(db.String(150))
    national_id = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    marital_status = db.Column(db.String(20))
    parent_name = db.Column(db.String(150))
    dob = db.Column(db.String(20))

    # Location Details
    country = db.Column(db.String(50))
    province = db.Column(db.String(50))
    district = db.Column(db.String(50))
    sector = db.Column(db.String(50))
    cell = db.Column(db.String(50))
    village = db.Column(db.String(50))

    # Church Responsibilities
    role = db.Column(db.String(100))
    baptized = db.Column(db.String(10))
    baptism_date = db.Column(db.String(20))
    itsinda = db.Column(db.String(50))
    status = db.Column(db.String(20))
    deactivation_reason = db.Column(db.String(200))


# ================= ROUTES =================

@app.route('/')
def home():
    return redirect(url_for('members'))


@app.route('/members')
def members():
    all_members = Member.query.all()
    return render_template('members.html', members=all_members)


@app.route('/add_member', methods=['POST'])
def add_member():
    try:
        data = request.form

        new_member = Member(
            # Personal Identification
            full_name=data.get('full_name'),
            national_id=data.get('national_id'),
            phone=data.get('phone'),
            gender=data.get('gender'),
            marital_status=data.get('marital_status'),
            parent_name=data.get('parent_name'),
            dob=data.get('dob'),

            # Location
            country=data.get('country'),
            province=data.get('province'),
            district=data.get('district'),
            sector=data.get('sector'),
            cell=data.get('cell'),
            village=data.get('village'),

            # Church
            role=data.get('role'),
            baptized=data.get('baptized'),
            baptism_date=data.get('baptism_date'),
            itsinda=data.get('itsinda'),
            status=data.get('status'),
            deactivation_reason=data.get('deactivation_reason')
        )

        db.session.add(new_member)
        db.session.commit()

        return redirect(url_for('members'))

    except Exception as e:
        print("ERROR:", e)
        return f"Error occurred: {e}", 500


# ================= INIT DB =================
with app.app_context():
    db.create_all()


# ================= RUN APP =================
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)