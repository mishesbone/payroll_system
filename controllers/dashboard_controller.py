from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.employee import Employee
from models.user import User
from models.payroll import Payroll
from models.attendance import Attendance
from models.company import Company
from models.department import Department
from models.leave import Leave

from app import db

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/', methods=['GET'])
@login_required
def dashboard():
    if not current_user:  
        flash("Unauthorized access!", "danger")
        return redirect(url_for('auth.login'))

    payrolls = Payroll.query.filter_by(user_id=current_user.id).all()
    attendance_records = Attendance.query.filter_by(user_id=current_user.id).all()
    employee = Employee.query.filter_by(user_id=current_user.id).first()
    leave = Leave.query.filter_by(user_id=current_user.id).first()

    
    # Fetch all companies for search feature
    companies = Company.query.all()

    return render_template(
        'dashboard/index.html', 
        payrolls=payrolls, 
        attendance_records=attendance_records, 
        employee=employee,
        companies=companies, leave=leave
    )

@dashboard_bp.route('/create_company', methods=['POST'])
@login_required
def create_company():
    company_name = request.form['company_name']

    # Check if company already exists
    existing_company = Company.query.filter_by(name=company_name).first()
    if existing_company:
        flash("Company already exists!", "warning")
        return redirect(url_for('dashboard.dashboard'))

    # Create new company & make user admin
    new_company = Company(name=company_name, admin_id=current_user.id)
    db.session.add(new_company)
    db.session.commit()

    # Assign user as Admin
    current_user.role = "Admin"
    db.session.commit()

    flash("Company created successfully! You are now the admin.", "success")
    return redirect(url_for('dashboard.dashboard'))

@dashboard_bp.route('/join_company/<int:company_id>', methods=['POST'])
@login_required
def join_company(company_id):
    company = Company.query.get(company_id)

    if not company:
        flash("Company not found!", "danger")
        return redirect(url_for('dashboard.dashboard'))

    # Check if user is already part of the company
    existing_employee = Employee.query.filter_by(user_id=current_user.id, company_id=company_id).first()
    if existing_employee:
        flash("You are already part of this company!", "info")
        return redirect(url_for('dashboard.dashboard'))

    # Add user as an employee
    new_employee = Employee(user_id=current_user.id, company_id=company_id)
    db.session.add(new_employee)
    db.session.commit()

    flash(f"You have joined {company.name} successfully!", "success")
    return redirect(url_for('dashboard.dashboard'))
@dashboard_bp.route('/manage_company', methods=['GET'])
@login_required
def manage_company():
    if current_user.role != "Admin":
        flash("Access Denied! Admins only.", "danger")
        return redirect(url_for('dashboard.dashboard'))

    company = Company.query.filter_by(admin_id=current_user.id).first()
    employees = Employee.query.filter_by(company_id=company.id).all() if company else []

    return render_template('dashboard/manage_company.html', company=company, employees=employees)

@dashboard_bp.route('/remove_employee/<int:user_id>', methods=['POST'])
@login_required
def remove_employee(user_id):
    if current_user.role != "Admin":
        flash("Access Denied!", "danger")
        return redirect(url_for('dashboard.dashboard'))

    employee = Employee.query.filter_by(user_id=user_id, company_id=current_user.company.id).first()
    if employee:
        db.session.delete(employee)
        db.session.commit()
        flash("Employee removed successfully!", "success")
    else:
        flash("Employee not found!", "danger")

    return redirect(url_for('dashboard.manage_company'))
