from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
import datetime

from models.payroll import Payroll

# Assuming you have database models for payroll data, employees, etc.
from models import Payroll, Employee
from app import db

payroll_bp = Blueprint('payroll', __name__)

@payroll_bp.route('/payroll', methods=['GET', 'POST'])
@login_required
def payroll_home():
    payroll_data = []

    if request.method == 'POST':
        employee_id = request.form.get('employee_id')
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')

        try:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

            # Fetch payroll data based on criteria
            
            if employee_id and start_date and end_date:
                payroll_data = Payroll.query.filter(Payroll.employee_id == employee_id,Payroll.pay_date >= start_date,Payroll.pay_date <= end_date).all()
            
            if employee_id and start_date and end_date:
                payroll_data = [
                    {'payroll_id': 1, 'employee_id': employee_id, 'pay_date': start_date, 'gross_pay': 5000, 'net_pay': 4000},
                    {'payroll_id': 2, 'employee_id': employee_id, 'pay_date': end_date, 'gross_pay': 5200, 'net_pay': 4200}
                ]
            elif employee_id:
                payroll_data = [
                    {'payroll_id': 3, 'employee_id': employee_id, 'pay_date': datetime.date(2023, 1, 15), 'gross_pay': 4800, 'net_pay': 3800}
                ]

            if not payroll_data:
                flash('No payroll data found for the given criteria.', 'info')

        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'error')

    return render_template('payroll.html', payroll_data=payroll_data)

@payroll_bp.route('/payroll/details/<int:payroll_id>')
@login_required
def payroll_details(payroll_id):
    # Fetch detailed payroll information
    payroll = Payroll.query.get_or_404(payroll_id)
    payroll = next((p for p in [
        {'payroll_id': 1, 'employee_id': '123', 'pay_date': datetime.date(2023, 1, 1), 'gross_pay': 5000, 'net_pay': 4000, 'deductions': [{'type': 'tax', 'amount': 500}, {'type': 'insurance', 'amount': 500}]},
        {'payroll_id': 2, 'employee_id': '123', 'pay_date': datetime.date(2023, 2, 1), 'gross_pay': 5200, 'net_pay': 4200, 'deductions': [{'type': 'tax', 'amount': 520}, {'type': 'insurance', 'amount': 480}]},
        {'payroll_id': 3, 'employee_id': '456', 'pay_date': datetime.date(2023, 1, 15), 'gross_pay': 4800, 'net_pay': 3800, 'deductions': [{'type': 'tax', 'amount': 480}, {'type': 'insurance', 'amount': 520}]}
    ] if p['payroll_id'] == payroll_id), None)

    if payroll:
        return render_template('payroll_details.html', payroll=payroll)
    else:
        flash('Payroll details not found.', 'error')
        return redirect(url_for('payroll.payroll'))