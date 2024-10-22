from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

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

    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        flash('Login successful', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Login failed. Check your email and password.', 'error')
        return redirect(url_for('login_signup_page'))

# Signup Route
@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['psw']

    # Check if the email is already registered
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash('Email already exists. Please login.', 'error')
        return redirect(url_for('login_signup_page'))

    # Hash the password before storing it
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    flash('Account created successfully', 'success')
    return redirect(url_for('login_signup_page'))

# A simple route for dashboard (requires user to be logged in)
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return "Welcome to your dashboard"
    else:
        return redirect(url_for('login_signup_page'))

# Route to render the login/signup page
@app.route('/')
def login_signup_page():
    return render_template('LoginSignin.html')

if __name__ == '__main__':
    app.run(debug=True)