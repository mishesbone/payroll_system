from flask import Blueprint, render_template, request, flash, redirect, send_from_directory, url_for
from flask_login import login_required, current_user
import datetime
# Assuming you have a database model for reports, adjust as needed
from models import PayrollReport
from app import db

report_bp = Blueprint('report', __name__)

@report_bp.route('/report', methods=['GET', 'POST'])
@login_required
def payroll_home():
    reports = []
    if current_user.is_admin: 
        if request.method == 'POST':
            report_type = request.form.get('report_type')
            start_date_str = request.form.get('start_date')
            end_date_str = request.form.get('end_date')

            try:
                start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
                end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

                # Fetch reports based on criteria
                
                if report_type == 'monthly' and start_date and end_date:
                    reports = PayrollReport.query.filter(PayrollReport.report_date >= start_date, PayrollReport.report_date <= end_date).all()

                
                if report_type == 'monthly' and start_date and end_date:
                    reports = [
                        {'report_id': 1, 'report_type': 'monthly', 'report_date': start_date, 'file_path': '/reports/monthly_1.pdf'},
                        {'report_id': 2, 'report_type': 'monthly', 'report_date': end_date, 'file_path': '/reports/monthly_2.pdf'}
                    ]
                elif report_type == 'employee' and start_date and end_date:
                    reports = [
                        {'report_id': 3, 'report_type': 'employee', 'report_date': start_date, 'file_path': '/reports/employee_1.pdf'},
                        {'report_id': 4, 'report_type': 'employee', 'report_date': end_date, 'file_path': '/reports/employee_2.pdf'}
                    ]

                if not reports:
                    flash('No reports found for the given criteria.', 'info')

            except ValueError:
                flash('Invalid date format. Please use YYYY-MM-DD.', 'error')

        return render_template('reports.html', reports=reports)
    else:
        flash('You do not have permission to view reports.', 'warning')
        return redirect(url_for('employee.employee_dashboard')) #Or admin dashboard

@report_bp.route('/report/download/<int:report_id>')
@login_required
def download_report(report_id):
    if current_user.is_admin:
        # Fetch the report from the database or wherever it's stored
        report = PayrollReport.query.get_or_404(report_id)
        
        report = next((r for r in [
            {'report_id': 1, 'report_type': 'monthly', 'report_date': datetime.date(2023, 1, 1), 'file_path': '/reports/monthly_1.pdf'},
            {'report_id': 2, 'report_type': 'monthly', 'report_date': datetime.date(2023, 2, 1), 'file_path': '/reports/monthly_2.pdf'},
            {'report_id': 3, 'report_type': 'employee', 'report_date': datetime.date(2023, 3, 1), 'file_path': '/reports/employee_1.pdf'},
            {'report_id': 4, 'report_type': 'employee', 'report_date': datetime.date(2023, 4, 1), 'file_path': '/reports/employee_2.pdf'}
        ] if r['report_id'] == report_id), None)
        if report:
            # Logic to send the file to the user
            return send_from_directory(app.config['UPLOAD_FOLDER'], report.file_path)
            
            flash(f"Download initiated for report ID: {report_id}", "success")
            return redirect(report['file_path']) 
        else:
            flash('Report not found.', 'error')
            return redirect(url_for('report.payroll_home'))
    else:
        flash('You do not have permission to download reports.', 'warning')
        return redirect(url_for('employee.employee_dashboard'))
    

