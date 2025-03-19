#controllers/__init__.py
from .dashboard_controller import dashboard_bp
from .auth_controller import auth_bp
from .admin_controller import admin_bp
from .employee_controller import employee_bp
from .company_controller import company_bp
from .leave_controller import leave_bp
from .payroll_controller import payroll_bp
from .attendance_controller import attendance_bp
from .department_controller import department_bp
from .role_controller import role_bp
from .report_controller import report_bp
from .user_controller import user_bp


# Register blueprints
blueprints = [
    dashboard_bp,
    auth_bp,
    admin_bp,
    employee_bp,
    company_bp,
    leave_bp,
    payroll_bp,
    attendance_bp,
    department_bp,
    role_bp,
    report_bp,
    user_bp
]

def register_blueprints(app):
    for bp in blueprints:
        app.register_blueprint(bp)

# You can add more initializations or imports as needed