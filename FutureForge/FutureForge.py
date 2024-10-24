from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dasikretki'

# Correct MySQL URI format
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Luisamaesy_1229@localhost/futureforge'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Login Route
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['psw']
    user = User.query.filter_by(email=email).first()

    if user and user.password == password:  # Compare the plain password
        session['user_id'] = user.id
        flash('Login successful', 'success')
        return redirect(url_for('skills_gap_report'))  # Redirect to SkillsGapReport.html
    else:
        flash('Login failed. Check your email and password.', 'error')
        return redirect(url_for('login_signup_page'))

# Signin Route
@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['psw']
    
    # Log the received values
    print(f"Received email: {email}, password: {password}")

    # Check if the email is already registered
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash('Email already exists. Please login.', 'error')
        return redirect(url_for('login_signup_page'))

    try:
        new_user = User(email=email, password=password)  # Store the plain password directly
        db.session.add(new_user)
        db.session.commit()  # Commit the changes to the database
        flash('Account created successfully', 'success')
        return redirect(url_for('skills_gap_report'))
    except Exception as e:
        db.session.rollback()  # Rollback the session on error
        flash(f'Error creating account: {str(e)}', 'error')

    return redirect(url_for('login_signup_page'))


# Routes to render

@app.route('/navbar')
def navbar():
    return render_template('navbar.html')

# Route to render the SkillsGapReport.html
@app.route('/skills-gap-report')
def skills_gap_report():
    return render_template('SkillsGapReport.html')

# Route to render the login/signup page
@app.route('/')
def login_signup_page():
    return render_template('LoginSignin.html')

if __name__ == '__main__':
    app.run(debug=True)
