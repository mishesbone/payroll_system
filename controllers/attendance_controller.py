#controllers/attendance_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from controllers.dashboard_controller import user_belongs_to_company
from models.attendance import Attendance
from models.employee import Employee
from models.payroll import Payroll
from models.leave import Leave
from models.company import Company


attendance_bp = Blueprint('attendance', __name__, url_prefix='/attendance')

@attendance_bp.route('/mark_attendance', methods=['POST'])
@login_required 
@user_belongs_to_company
def mark_attendance():
    user_id = current_user.id
    employee = Employee.query.filter_by(user_id=user_id).first()
    company = Company.query.get(employee.company_id)
    attendance_date = request.form['attendance_date']
    time_in = request.form['time_in']
    time_out = request.form['time_out']
    remarks = request.form['remarks']

    new_attendance = Attendance(
        user_id=user_id, 
        company_id=company.id,
        attendance_date=attendance_date, 
        time_in=time_in, 
        time_out=time_out, 
        remarks=remarks
    )
    try:
        db.session.add(new_attendance)
        db.session.commit()
        flash("Attendance marked successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error marking attendance: {str(e)}", "danger")
    
    return redirect(url_for('dashboard.dashboard'))

@attendance_bp.route('/view_attendance', methods=['GET'])
@login_required
@user_belongs_to_company
def view_attendance():
    if not current_user.is_admin:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('auth.login'))
    
    attendance_records = Attendance.query.all()
    return render_template('attendance/view_attendance.html', attendance_records=attendance_records)

@attendance_bp.route('/edit_attendance/<int:attendance_id>', methods=['POST'])
@login_required
def edit_attendance(attendance_id):
    attendance = Attendance.query.get_or_404(attendance_id)

    attendance.attendance_date = request.form['attendance_date']
    attendance.time_in = request.form['time_in']
    attendance.time_out = request.form['time_out']
    attendance.remarks = request.form['remarks']

    db.session.commit()
    flash("Attendance updated successfully!", "success")
    return redirect(url_for('attendance.view_attendance'))

@attendance_bp.route('/delete_attendance/<int:attendance_id>', methods=['POST'])
@login_required
@user_belongs_to_company
def delete_attendance(attendance_id):
    attendance = Attendance.query.get_or_404(attendance_id)
    db.session.delete(attendance)
    db.session.commit()

    flash("Attendance deleted successfully!", "success")
    return redirect(url_for('attendance.view_attendance'))

@attendance_bp.route('/export', methods=['GET'])
@login_required
@user_belongs_to_company
def export_attendance():
    if not current_user.is_admin:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('auth.login'))
    
    attendance_records = Attendance.query.all()
    # Logic to export attendance records to CSV
    return jsonify({"message": "Exporting attendance records to CSV"})

