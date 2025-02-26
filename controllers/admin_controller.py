#payroll_system/admin_controller.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.user import User
from models.employee import Employee
from models.payroll import Payroll
from models.attendance import Attendance
from models.leave import Leave
from services.email_service import EmailService as send_email
from app import db

# Blueprint for admin functionalities
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin dashboard
@admin_bp.route('/')
@login_required
def dashboard():
    if not current_user.is_admin:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('auth.login'))
    
    employees = Employee.query.count()
    payrolls = Payroll.query.count()
    leaves = Leave.query.count()
    users = User.query.count()
    
    return render_template('dashboard/admin_dashboard.html', employees=employees, payrolls=payrolls, leaves=leaves, users=users)

# Manage users
@admin_bp.route('/users')
@login_required
def manage_users():
    if not current_user.is_admin:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('auth.login'))
    
    users = User.query.all()
    return render_template('admin/users.html', users=users)

# Update user role
@admin_bp.route('/users/update_role/<int:user_id>', methods=['POST'])
@login_required
def update_user_role(user_id):
    if not current_user.is_admin:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('auth.login'))

    user = User.query.get_or_404(user_id)
    new_role = request.form.get('role')

    if new_role in ["admin", "employee", "manager"]:
        user.role = new_role
        db.session.commit()
        flash(f"Role updated to {new_role} for {user.username}", "success")
    else:
        flash("Invalid role!", "danger")

    return redirect(url_for('admin.manage_users'))

# Delete user
@admin_bp.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('auth.login'))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully!", "success")

    return redirect(url_for('admin.manage_users'))

# Approve payroll
@admin_bp.route('/payroll/approve/<int:payroll_id>', methods=['POST'])
@login_required
def approve_payroll(payroll_id):
    if not current_user.is_admin:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('auth.login'))

    payroll = Payroll.query.get_or_404(payroll_id)
    payroll.status = "Approved"
    db.session.commit()
    
    # Notify employee
    employee = Employee.query.get(payroll.employee_id)
    send_email(
        subject="Payroll Approved",
        recipient=employee.email,
        body=f"Dear {employee.name}, your payroll for {payroll.month} has been approved."
    )

    flash("Payroll approved successfully!", "success")
    return redirect(url_for('admin.dashboard'))

# System settings page
@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if not current_user.is_admin:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        # Handle settings update logic (e.g., tax rates, payroll cycle)
        flash("Settings updated successfully!", "success")
        return redirect(url_for('admin.settings'))

    return render_template('admin/settings.html')

# Fetch system statistics (API endpoint)
@admin_bp.route('/api/stats', methods=['GET'])
@login_required
def get_statistics():
    if not current_user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403

    stats = {
        "employees": Employee.query.count(),
        "payrolls": Payroll.query.count(),
        "leaves": Leave.query.count(),
        "users": User.query.count()
    }
    return jsonify(stats)
