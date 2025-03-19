from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_required, current_user, login_user
from sqlalchemy.orm import joinedload
from functools import wraps

from models.employee import Employee
from models.user import User
from models.payroll import Payroll
from models.attendance import Attendance
from models.company import Company
from models.department import Department
from models.leave import Leave
from models.paycode import Paycode
from models.deduction import Deduction
from models.benefit import Benefit
from models.payslip import PaySlip
from models.user_company import UserCompany  # Ensure these exist

from app import db

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


# Ensure user belongs to the company before accessing dashboard
def user_belongs_to_company(f):
    @wraps(f)
    def decorated_function(company_id, *args, **kwargs):
        user_company = UserCompany.query.filter_by(user_id=current_user.id, company_id=company_id).first()
        if not user_company:
            flash("Unauthorized access!", "danger")
            return redirect(url_for('dashboard.dashboard_home'))
        return f(company_id, *args, **kwargs)
    return decorated_function


@dashboard_bp.route('/<int:company_id>/<int:user_id>', methods=['GET', 'POST'])
@login_required
@user_belongs_to_company
def company_dashboard(company_id, user_id):
    session['user_id'] = user_id 
    company = Company.query.get(company_id)
    users = User.query.filter_by(company_id=company_id).all()
    employees = Employee.query.filter_by(company_id=company_id).all()
    pay_codes = Paycode.query.filter_by(company_id=company_id).all()
    deductions = Deduction.query.filter_by(company_id=company_id).all()
    benefits = Benefit.query.filter_by(company_id=company_id).all()
    monthly_payroll_records = Payroll.query.filter_by(company_id=company_id).all()
    pay_slips = PaySlip.query.filter_by(company_id=company_id).all()

    return render_template('dashboard.html', user_id=user_id, company=company, users=users, 
                           employees=employees, company_id=company_id, pay_codes=pay_codes,
                           deductions=deductions, benefits=benefits, monthly_payroll_records=monthly_payroll_records,
                           pay_slips=pay_slips)


@dashboard_bp.route('/user/<int:user_id>')
@login_required
def user_dashboard(user_id):
    user = User.query.get(user_id)
    if not user:
        return render_template('404.html'), 404

    login_user(user)

    user_company = UserCompany.query.filter_by(user_id=user.id).first()
    company_id = user_company.company_id if user_company else None

    return render_template('user_dashboard.html', user=user, company_id=company_id)


@dashboard_bp.route('/', methods=['GET'])
@login_required
def dashboard_home():
    if not current_user:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('auth.login'))

    payrolls = Payroll.query.filter_by(user_id=current_user.id).all()
    attendance_records = Attendance.query.filter_by(user_id=current_user.id).all()
    employee = Employee.query.filter_by(user_id=current_user.id).first()
    leave = Leave.query.filter_by(user_id=current_user.id).first()
    companies = Company.query.all()

    return render_template('dashboard/index.html', payrolls=payrolls, attendance_records=attendance_records,
                           employee=employee, companies=companies, leave=leave)


@dashboard_bp.route('/create_company', methods=['POST'])
@login_required
def create_company():
    company_name = request.form.get('company_name')

    if Company.query.filter_by(name=company_name).first():
        flash("Company already exists!", "warning")
        return redirect(url_for('dashboard.dashboard_home'))

    new_company = Company(name=company_name, admin_id=current_user.id)
    db.session.add(new_company)
    db.session.commit()

    current_user.role = "Admin"
    db.session.commit()

    flash("Company created successfully! You are now the admin.", "success")
    return redirect(url_for('dashboard.dashboard_home'))


@dashboard_bp.route('/join_company/<int:company_id>', methods=['POST'])
@login_required
def join_company(company_id):
    company = Company.query.get(company_id)
    if not company:
        flash("Company not found!", "danger")
        return redirect(url_for('dashboard.dashboard_home'))

    if Employee.query.filter_by(user_id=current_user.id, company_id=company_id).first():
        flash("You are already part of this company!", "info")
        return redirect(url_for('dashboard.dashboard_home'))

    new_employee = Employee(user_id=current_user.id, company_id=company_id)
    db.session.add(new_employee)
    db.session.commit()

    flash(f"You have joined {company.name} successfully!", "success")
    return redirect(url_for('dashboard.dashboard_home'))


@dashboard_bp.route('/manage_company', methods=['GET'])
@login_required
def manage_company():
    if current_user.role != "Admin":
        flash("Access Denied! Admins only.", "danger")
        return redirect(url_for('dashboard.dashboard_home'))

    company = Company.query.filter_by(admin_id=current_user.id).first()
    employees = Employee.query.filter_by(company_id=company.id).all() if company else []

    return render_template('dashboard/manage_company.html', company=company, employees=employees)


@dashboard_bp.route('/remove_employee/<int:user_id>', methods=['POST'])
@login_required
def remove_employee(user_id):
    if current_user.role != "Admin":
        flash("Access Denied!", "danger")
        return redirect(url_for('dashboard.dashboard_home'))

    employee = Employee.query.filter_by(user_id=user_id, company_id=current_user.company.id).first()
    if employee:
        db.session.delete(employee)
        db.session.commit()
        flash("Employee removed successfully!", "success")
    else:
        flash("Employee not found!", "danger")

    return redirect(url_for('dashboard.manage_company'))


@dashboard_bp.route('/export', methods=['GET'])
@login_required
@user_belongs_to_company
def export_dashboard():
    # Logic to export dashboard data to CSV
    return jsonify({"message": "Exporting dashboard data to CSV"})
