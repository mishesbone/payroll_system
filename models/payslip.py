#models/payslip.py
from app import db
from models.deduction import Deduction
from models.employee import Employee
from models.payroll import Payroll
from models.benefit import Benefit
from datetime import datetime
from sqlalchemy import ForeignKey

class PaySlip(db.Model):
    __tablename__ = 'payslips'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, ForeignKey('employees.id'), nullable=False)
    payroll_id = db.Column(db.Integer, ForeignKey('payrolls.id'), nullable=False)
    gross_salary = db.Column(db.Float, nullable=False)
    net_salary = db.Column(db.Float, nullable=False)
    total_deductions = db.Column(db.Float, nullable=False)
    total_benefits = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    employee = db.relationship('Employee', backref=db.backref('payslips', lazy=True))
    payroll = db.relationship('Payroll', backref=db.backref('payslips', lazy=True))
    benefits = db.relationship('Benefit', backref=db.backref('payslips', lazy=True))
    deductions = db.relationship('Deduction', backref=db.backref('payslips', lazy=True))

    def __repr__(self):
        return f"<PaySlip {self.id}, Employee: {self.employee_id}, Payroll: {self.payroll_id}>"

    def __str__(self):
        return f"PaySlip {self.id}"

