from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from controllers.dashboard_controller import user_belongs_to_company
from models.user import User
from models.attendance import Attendance
from models.department import  Department
from models.role import Role
from models.leave import Leave
from models.employee import Employee
from models.payroll import Payroll 
from models.company import Company
from services.email_service import EmailService as send_email
from forms.auth_forms import RegistrationForm, LoginForm, ResetPasswordForm  
from app import db
from sqlalchemy.exc import SQLAlchemyError



# Blueprint for admin functionalities
company_bp = Blueprint('company', __name__, url_prefix='/company')

# Admin dashboard
@company_bp.route('/')
@login_required
@user_belongs_to_company
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
@company_bp.route('/users')
@login_required
@user_belongs_to_company
def manage_users():
    if not current_user.is_admin:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('auth.login'))
    
    users = User.query.all()
    return render_template('admin/users.html', users=users)

# Update user role
@company_bp.route('/users/update_role/<int:user_id>', methods=['POST'])
@login_required
@user_belongs_to_company
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
@company_bp.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
@user_belongs_to_company
def delete_user(user_id):
    if not current_user.is_admin:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('auth.login'))
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    flash(f"User {user.username} deleted successfully!", "success")
    return redirect(url_for('admin.manage_users'))

# Add new company
@company_bp.route('/add', methods=['GET', 'POST'])
@login_required
@user_belongs_to_company
def add_company():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        
        new_company = Company(name=name, email=email, address=address)
        try:
            db.session.add(new_company)
            db.session.commit()
            flash("Company added successfully!", "success")
            return redirect(url_for('company.list_companies'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Error adding company: {str(e)}", "danger")
    
    return render_template('company/add.html')

# List all companies
@company_bp.route('/companies')
@login_required
@user_belongs_to_company
def list_companies():
    companies = Company.query.all()
    return render_template('company/list.html', companies=companies)

# Edit company details
@company_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@user_belongs_to_company
def edit_company(id):
    company = Company.query.get_or_404(id)
    
    if request.method == 'POST':
        company.name = request.form['name']
        company.email = request.form['email']
        company.address = request.form['address']
        
        try:
            db.session.commit()
            flash("Company updated successfully!", "success")
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Error updating company: {str(e)}", "danger")
    
    return render_template('company/edit.html', company=company)

# Delete company
@company_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
@user_belongs_to_company
def delete_company(id):
    company = Company.query.get_or_404(id)
    db.session.delete(company)
    db.session.commit()
    
    flash("Company deleted successfully!", "success")
    return redirect(url_for('company.list_companies'))


# View company profile
@company_bp.route('/<int:id>')
@login_required
@user_belongs_to_company
def profile_company(id):
    company = Company.query.get_or_404(id)
    return render_template('company/profile.html', company=company)

# Export companies
@company_bp.route('/export', methods=['GET'])
@login_required
@user_belongs_to_company
def export_companies():
    if not current_user.is_admin:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('auth.login'))
    
    # Export companies to CSV
    return jsonify({"message": "Exporting companies to CSV"})


# Add new employee
@company_bp.route('/employees/add', methods=['GET', 'POST'])
@login_required
@user_belongs_to_company
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        position = request.form['position']
        
        new_employee = Employee(name=name, email=email, position=position)
        try:
            db.session.add(new_employee)
            db.session.commit()
            flash("Employee added successfully!", "success")
            return redirect(url_for('company.list_employees'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Error adding employee: {str(e)}", "danger")
    
    return render_template('employee/add.html')

# List all employees
@company_bp.route('/employees')
@login_required
@user_belongs_to_company
def list_employees():
    employees = Employee.query.all()
    return render_template('employee/list.html', employees=employees)

# Edit employee details
@company_bp.route('/employees/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@user_belongs_to_company
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    
    if request.method == 'POST':
        employee.name = request.form['name']
        employee.email = request.form['email']
        employee.position = request.form['position']
        
        try:
            db.session.commit()
            flash("Employee updated successfully!", "success")
            return redirect(url_for('company.list_employees'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Error updating employee: {str(e)}", "danger")
    
    return render_template('employee/edit.html', employee=employee)

# View employee profile
@company_bp.route('/employees/<int:id>')
@login_required
@user_belongs_to_company
def profile_employee(id):
    employee = Employee.query.get_or_404(id)
    return render_template('employee/profile.html', employee=employee)

# Export employees
@company_bp.route('/employees/export', methods=['GET'])
@login_required
@user_belongs_to_company
def export_employees():
    if not current_user.is_admin:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('auth.login'))
    
    # Export employees to CSV
    return jsonify({"message": "Exporting employees to CSV"})


# Add new payroll
@company_bp.route('/payroll/add', methods=['GET', 'POST'])
@login_required
@user_belongs_to_company
def add_payroll():
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        pay_date = request.form['pay_date']
        amount = request.form['amount']
        status = request.form['status']
        
        new_payroll = Payroll(employee_id=employee_id, pay_date=pay_date, amount=amount, status=status)
        try:
            db.session.add(new_payroll)
            db.session.commit()
            flash("Payroll added successfully!", "success")
            return redirect(url_for('company.list_payrolls'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Error adding payroll: {str(e)}", "danger")
    
    return render_template('payroll/add.html')


# List all payrolls
@company_bp.route('/payrolls')
@login_required
@user_belongs_to_company
def list_payrolls():
    payrolls = Payroll.query.all()
    return render_template('payroll/list.html', payrolls=payrolls)

# Edit payroll details
@company_bp.route('/payrolls/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@user_belongs_to_company
def edit_payroll(id):
    payroll = Payroll.query.get_or_404(id)
    
    if request.method == 'POST':
        payroll.employee_id = request.form['employee_id']
        payroll.pay_date = request.form['pay_date']
        payroll.amount = request.form['amount']
        payroll.status = request.form['status']
        
        try:
            db.session.commit()
            flash("Payroll updated successfully!", "success")
            return redirect(url_for('company.list_payrolls'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Error updating payroll: {str(e)}", "danger")
    
    return render_template('payroll/edit.html', payroll=payroll)

# View payroll details
@company_bp.route('/payrolls/<int:id>')
@login_required
@user_belongs_to_company
def view_payroll(id):
    payroll = Payroll.query.get_or_404(id)
    return render_template('payroll/view.html', payroll=payroll)

# Export payrolls
@company_bp.route('/payrolls/export', methods=['GET'])
@login_required
@user_belongs_to_company
def export_payrolls():
    if not current_user.is_admin:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('auth.login'))
