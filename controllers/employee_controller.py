from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app import db
from sqlalchemy.exc import SQLAlchemyError

from models.attendance import Attendance
from models.employee import Employee
from models.payroll import Payroll

# Create Blueprint
employee_bp = Blueprint('employee', __name__)

    

# Employee Dashboard (User-specific records)
@employee_bp.route('/employee_dashboard', methods=['GET'])
@login_required
def employee_dashboard():
    if not current_user.is_employee:  
        flash("Unauthorized access!", "danger")
        return redirect(url_for('auth.login'))

    # Fetch records specific to the logged-in employee
    payrolls = Payroll.query.filter_by(user_id=current_user.id).all()
    attendance_records = Attendance.query.filter_by(user_id=current_user.id).all()
    employee = Employee.query.filter_by(user_id=current_user.id).first()

    return render_template(
        'dashboard/employee_dashboard.html', 
        payrolls=payrolls, 
        attendance_records=attendance_records, 
        employee=employee
    )

# List all employees
@employee_bp.route('/employees')
@login_required
def list_employees():
    employees = Employee.query.all()
    return render_template('employee/list.html', employees=employees)

# Add new employee
@employee_bp.route('/employees/add', methods=['GET', 'POST'])
@login_required
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
            return redirect(url_for('employee.list_employees'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Error adding employee: {str(e)}", "danger")
    
    return render_template('employee/add.html')

# Edit employee details
@employee_bp.route('/employees/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    
    if request.method == 'POST':
        employee.name = request.form['name']
        employee.email = request.form['email']
        employee.position = request.form['position']
        
        try:
            db.session.commit()
            flash("Employee updated successfully!", "success")
            return redirect(url_for('employee.list_employees'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Error updating employee: {str(e)}", "danger")
    
    return render_template('employee/edit.html', employee=employee)

# View employee profile
@employee_bp.route('/employees/<int:id>')
@login_required
def profile_employee(id):
    employee = Employee.query.get_or_404(id)
    return render_template('employee/profile.html', employee=employee)