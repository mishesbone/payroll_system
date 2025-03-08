from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from services.email_service import EmailService as send_email
from forms.auth_forms import RegistrationForm, LoginForm, ResetPasswordForm  
from app import db

from auth.oauth import google_bp  # ✅ Correct import


# Blueprint for authentication
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from models import User
from app import db, mail  # Ensure `mail` is set up in `app.py`


auth_bp = Blueprint("auth", __name__)
serializer = URLSafeTimedSerializer("YOUR_SECRET_KEY")  # Change to a secure key

def send_verification_email(user):
    """Send an email with a verification link."""
    token = serializer.dumps(user.email, salt="email-confirmation")
    user.verification_token = token  # Store token in DB
    db.session.commit()

    confirm_url = url_for('auth.verify_email', token=token, _external=True)
    msg = Message(
        "Confirm Your Email",
        sender="your_email@example.com",
        recipients=[user.email]
    )
    msg.body = f"Hello {user.username},\n\nPlease verify your email by clicking the link below:\n{confirm_url}\n\nIf you did not request this, please ignore it."
    mail.send(msg)

from flask import jsonify

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        username = form.username.data.strip()
        password = form.password.data
        accept_terms = form.accept_terms.data

        if not accept_terms:
            return jsonify({"success": False, "message": "You must accept the Terms and Conditions."}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"success": False, "message": "This email is already registered."}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"success": False, "message": "This username is already taken."}), 400

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

        new_user = User(
            email=email, username=username, password=hashed_password,
            role="user", accepted_terms=True, is_enabled=False
        )
        db.session.add(new_user)
        db.session.commit()

        send_verification_email(new_user)

        return jsonify({"success": True, "message": "Account created! Check your email.", "redirect_url": "/dashboard"}), 200

    return render_template('auth/register.html', form=form)  # Render template only for GET requests

@auth_bp.route('/verify_email/<token>')
def verify_email(token):
    try:
        email = serializer.loads(token, salt="email-confirmation", max_age=3600)  # Token expires in 1 hour
        user = User.query.filter_by(email=email).first()

        if user:
            user.is_enabled = True
            user.verification_token = None  # Clear token after verification
            db.session.commit()
            flash("Your email has been verified! You can now log in.", "success")
            return redirect(url_for('auth.login'))
        else:
            flash("Invalid or expired verification link.", "danger")
            return redirect(url_for('auth.register'))

    except SignatureExpired:
        flash("The verification link has expired. Please register again.", "danger")
        return redirect(url_for('auth.register'))


# 🔹 Login Route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login successful!", "success")

            # Redirect based on user role
            if user.role == "admin":
                return redirect(url_for('dashboard.admin_dashboard'))
            return redirect(url_for('dashboard.employee_dashboard'))

        flash("Invalid email or password!", "danger")

    return render_template('auth/login.html', form=form)

# Logout route
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "success")
    return redirect(url_for('auth.login'))


# Password reset request
@auth_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("No account found with that email!", "danger")
            return redirect(url_for('auth.reset_password'))

        reset_token = user.generate_reset_token()
        reset_url = url_for('auth.reset_password_token', token=reset_token, _external=True)
        
        send_email(
            subject="Password Reset Request",
            recipient=email,
            body=f"Click the link below to reset your password:\n\n{reset_url}"
        )

        flash("A password reset link has been sent to your email.", "info")
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html')

# Password reset confirmation
@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password_token(token):
    user = User.verify_reset_token(token)
    
    if not user:
        flash("Invalid or expired token!", "danger")
        return redirect(url_for('auth.reset_password'))

    if request.method == 'POST':
        new_password = request.form.get('password')
        user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
        db.session.commit()

        flash("Password reset successfully! You can now log in.", "success")
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password_token.html')
