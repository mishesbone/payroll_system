from datetime import datetime
from app import db

from .user import User

class Payroll(db.Model):
    __tablename__ = 'payrolls'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    basic_salary = db.Column(db.Float, default=0.0)
    overtime_hours = db.Column(db.Float, default=0.0)
    overtime_rate = db.Column(db.Float, default=0.0)
    overtime_amount = db.Column(db.Float, default=0.0)
    allowances = db.Column(db.Float, default=0.0)
    bonuses = db.Column(db.Float, default=0.0)
    gross_salary = db.Column(db.Float, default=0.0)
    tax_deduction = db.Column(db.Float, default=0.0)
    insurance_deduction = db.Column(db.Float, default=0.0)
    other_deductions = db.Column(db.Float, default=0.0)
    total_deductions = db.Column(db.Float, default=0.0)
    net_salary = db.Column(db.Float, default=0.0)
    payment_date = db.Column(db.Date, nullable=True)
    payment_method = db.Column(db.String(20), default='bank_transfer')  # bank_transfer, cash, check
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, cancelled
    remarks = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    employee = db.relationship('Employee', back_populates='payrolls')
    creator = db.relationship('User', foreign_keys=[created_by])
    approver = db.relationship('User', foreign_keys=[approved_by])

    def __repr__(self):
        return f'<Payroll {self.employee.employee_id} - {self.month}/{self.year}>'

    @property
    def period(self):
        return f"{self.month}/{self.year}"

class PayrollReport(db.Model):
    __tablename__ = 'payroll_reports'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    total_employees = db.Column(db.Integer, default=0)
    total_payrolls = db.Column(db.Integer, default=0)
    total_gross_salary = db.Column(db.Float, default=0.0)
    total_net_salary = db.Column(db.Float, default=0.0)
    total_tax_deduction = db.Column(db.Float, default=0.0)
    total_insurance_deduction = db.Column(db.Float, default=0.0)
    total_other_deductions = db.Column(db.Float, default=0.0)
    total_deductions = db.Column(db.Float, default=0.0)
    total_overtime_hours = db.Column(db.Float, default=0.0)
    total_overtime_amount = db.Column(db.Float, default=0.0)
    total_allowances = db.Column(db.Float, default=0.0)
    total_bonuses = db.Column(db.Float, default=0.0)
    total_payment = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = db.relationship('Company', back_populates='payroll_reports')

    def __repr__(self):
        return f'<PayrollReport {self.month}/{self.year}>'

    @property
    def period(self):
        return f"{self.month}/{self.year}"

    @property
    def total_employees(self):
        return self.total_employees

    @property
    def total_payrolls(self):
        return self.total_payrolls

    @property
    def total_gross_salary(self):
        return self.total_gross_salary

    @property
    def total_net_salary(self):
        return self.total_net_salary

    @property
    def total_tax_deduction(self):
        return self.total_tax_deduction

    @property
    def total_insurance_deduction(self):
        return self.total_insurance_deduction

class PayrollDeduction(db.Model):
    __tablename__ = 'payroll_deductions'

    id = db.Column(db.Integer, primary_key=True)
    payroll_id = db.Column(db.Integer, db.ForeignKey('payrolls.id'), nullable=False)
    deduction_type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, default=0.0)
    remarks = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    payroll = db.relationship('Payroll', back_populates='deductions')

    def __repr__(self):
        return f'<PayrollDeduction {self.deduction_type} - {self.amount}>'

# Add back_populates to Payroll relationship with PayrollDeduction
Payroll.deductions = db.relationship('PayrollDeduction', back_populates='payroll', cascade='all, delete-orphan')

