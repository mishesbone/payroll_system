from flask import Blueprint, redirect, url_for, flash
from flask_login import login_user
from flask_dance.contrib.google import make_google_blueprint, google

# Google OAuth Blueprint
google_bp = make_google_blueprint(
    client_id="YOUR_GOOGLE_CLIENT_ID",
    client_secret="YOUR_GOOGLE_CLIENT_SECRET",
    redirect_to="oauth.google_callback",
    scope=["openid", "email", "profile"]
)

oauth_bp = Blueprint("oauth", __name__, url_prefix="/oauth")


@oauth_bp.route("/google_callback")
def google_callback():
    if not google.authorized:
        return redirect(url_for("google_bp.login"))  # Redirect to Google OAuth login

    resp = google.get("/oauth2/v1/userinfo")  # Get user info from Google
    if resp.ok:
        user_info = resp.json()
        email = user_info["email"]
        username = user_info.get("name", email.split("@")[0])

        # ✅ Import `db` and `User` inside the function to avoid circular import
        from app import db
        from models import User

        # Check if user exists
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email, username=username, role="user", accepted_terms=True)  
            db.session.add(user)
            db.session.commit()

        login_user(user)
        flash("Logged in successfully!", "success")
        return redirect(url_for("dashboard.index"))

    flash("Failed to authenticate with Google.", "danger")
    return redirect(url_for("auth.login"))
