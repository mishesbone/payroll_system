import os
import logging
from celery import Celery
from flask import Flask, render_template, redirect, url_for, send_from_directory, request, flash
from extensions import db, migrate, login_manager, mail, celery, csrf  # Import extensions from extensions module
from config import get_config
from auth.oauth import google_bp, oauth_bp
from models.user import User
from models.role import Role

# Configure Logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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

    app.config['SESSION_TYPE'] = 'filesystem'
    
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
    from controllers.attendance_controller import attendance_bp
    from controllers.department_controller import department_bp
    from controllers.role_controller import role_bp
    from controllers.leave_controller import leave_bp
    from controllers.user_controller import user_bp
    from controllers.services import services_bp
    from controllers.products import products_bp
    from controllers.downloads import downloads_bp
    
    from auth.oauth import oauth_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(payroll_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(oauth_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(department_bp)
    app.register_blueprint(role_bp)
    app.register_blueprint(leave_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(downloads_bp)
    
    app.register_blueprint(google_bp, url_prefix="/login")
    
    # Import User model here to avoid circular import
    from models.user import User

    # Serve static files
    @app.route('/static/<path:filename>')
    def static_files(filename):
        return send_from_directory('static', filename)

    # Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html', user_id=1), 404  # Provide a default user_id

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

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            role = request.form['role']

            if password != confirm_password:
                flash('Passwords do not match', 'danger')
                return redirect(url_for('auth.register'))

            user = User(username=username, email=email)
            user.set_password(password)
            user.role = Role.query.filter_by(name=role).first()

            db.session.add(user)
            db.session.commit()

            flash('Registration successful', 'success')
            if role == 'admin':
                return redirect(url_for('dashboard.admin_dashboard'))
            else:
                return redirect(url_for('dashboard.employee_dashboard'))

        return render_template('auth/register.html')

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