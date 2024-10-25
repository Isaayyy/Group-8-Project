from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import random 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dasikretki'

# MySQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Luisamaesy_1229@localhost/futureforge'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Flask-Mail configuration for Gmail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465  # Or 587 if using TLS
app.config['MAIL_USERNAME'] = 'futureforge1024@gmail.com'
app.config['MAIL_PASSWORD'] = 'FForge@1024'
app.config['MAIL_USE_TLS'] = False 
app.config['MAIL_USE_SSL'] = True 
mail = Mail(app)

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


# Forgot Password Route
@app.route('/send-verification-email', methods=['POST'])
def send_verification_email():
    email = request.form['email']
    
    # Generate a random 6-digit verification number
    confirmation_number = ''.join([str(random.randint(0, 9)) for _ in range(6)])

    # Store the confirmation number in the session
    session['confirmation_number'] = confirmation_number  # Store for later comparison
    
    # Prepare the email message
    msg = Message(
        'Password Reset Request',
        sender='futureforge1024@gmail.com',
        recipients=[email]
    )
    
    # Create the email body
    msg.body = f'Your verification number is: {confirmation_number}\n\nUse this number to reset your password.'
    
    try:
        # Send the email
        mail.send(msg)
        flash('A verification number has been sent to your email.', 'success')
    except Exception as e:
        flash(f'Error sending email: {str(e)}', 'error')

    return redirect(url_for('login_signup_page'))

@app.route('/enter-number', methods=['POST'])
def enter_number():
    entered_number = request.form['confirmation_number']
    
    # Retrieve the confirmation number from the session
    confirmation_number = session.get('confirmation_number')  # Get confirmation number from session

    if entered_number == confirmation_number:  # Compare with the session value
        return redirect(url_for('enter_new_pass'))  # Proceed to enter new password
    else:
        flash('Incorrect number. Please try again.', 'error')
        return redirect(url_for('login_signup_page'))  # Redirect to the login page

# Change Password Route
@app.route('/change-password', methods=['POST'])
def change_password():
    new_pass = request.form['newPass']
    confirm_pass = request.form['confirmPass']

    if new_pass == confirm_pass:
        # Retrieve the user from the session
        user = User.query.get(session['user_id'])

        if user:  # Ensure user exists
            user.password = new_pass  # Store the plain password directly
            db.session.commit()
            flash('Password updated successfully', 'success')
            return redirect(url_for('skills_gap_report'))
        else:
            flash('User not found. Please log in again.', 'error')
            return redirect(url_for('login_signup_page'))  # Redirect to login page if user is not found
    else:
        flash('Passwords do not match', 'error')
        return redirect(url_for('enter_new_pass'))


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
