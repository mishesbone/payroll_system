import os
import logging
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from celery import Celery
from config import get_config
from flask_wtf.csrf import CSRFProtect
from auth.oauth import google_bp, oauth_bp


# Configure Logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Define Flask extensions globally
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
celery = Celery()
csrf = CSRFProtect()




def create_app():
    """Flask app factory function."""
    app = Flask(__name__)
    app.config.from_object(get_config())
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = "your_email@example.com"
    app.config["MAIL_PASSWORD"] = "your_email_password"  # Use environment variables instead!
    app.config["MAIL_DEFAULT_SENDER"] = "your_email@example.com"



    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    mail.init_app(app)
    csrf.init_app(app)

    # Register blueprints
    from controllers.auth_controller import auth_bp
    from controllers.employee_controller import employee_bp
    from controllers.payroll_controller import payroll_bp
    from controllers.report_controller import report_bp
    from controllers.admin_controller import admin_bp
    from controllers.dashboard_controller import dashboard_bp
    from auth.oauth import oauth_bp
    

    app.register_blueprint(auth_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(payroll_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(oauth_bp)
    app.register_blueprint(google_bp, url_prefix="/login")
    


    


    # Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        logging.warning(f"404 Error: {e}")
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        logging.error(f"500 Error: {e}", exc_info=True)
        return render_template('errors/500.html'), 500

    # Root Route
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    # Flask-Login User Loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

def create_celery(app=None):
    """Create a Celery instance for background tasks."""
    app = app or create_app()
    celery = Celery(
        app.import_name,
        backend=app.config.get('CELERY_RESULT_BACKEND'),
        broker=app.config.get('CELERY_BROKER_URL')
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        """Ensure Celery tasks have Flask app context."""
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

if __name__ == '__main__':
    app = create_app()
    celery = create_celery(app)  # Initialize Celery globally

    app.run(host='0.0.0.0', port=5000, debug=app.config.get('DEBUG', False))
