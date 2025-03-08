from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app import db

class Payroll(db.Model):
    __tablename__ = 'payrolls'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, ForeignKey('employees.id'), nullable=False)
    basic_salary = db.Column(db.Float, nullable=False)
    bonuses = db.Column(db.Float, default=0.0)
    deductions = db.Column(db.Float, default=0.0)
    net_salary = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    employee = db.relationship('Employee', back_populates='payrolls')
    benefits = db.relationship('PayrollBenefit', back_populates='payroll', cascade='all, delete-orphan')
    other_deductions = db.relationship('PayrollOtherDeduction', back_populates='payroll', cascade='all, delete-orphan')

class PayrollBenefit(db.Model):
    __tablename__ = 'payroll_benefits'
    id = db.Column(db.Integer, primary_key=True)
    payroll_id = db.Column(db.Integer, ForeignKey('payrolls.id'), nullable=False)
    benefit_type = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    payroll = db.relationship('Payroll', back_populates='benefits')

class PayrollOtherDeduction(db.Model):
    __tablename__ = 'payroll_other_deductions'
    id = db.Column(db.Integer, primary_key=True)
    payroll_id = db.Column(db.Integer, ForeignKey('payrolls.id'), nullable=False)
    amount = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    payroll = db.relationship('Payroll', back_populates='other_deductions')

class PayrollReport(db.Model):
    __tablename__ = 'payroll_reports'
    id = db.Column(db.Integer, primary_key=True)
    total_employees = db.Column(db.Integer, nullable=False, default=0)
    total_payrolls = db.Column(db.Integer, nullable=False, default=0)
    total_salaries_paid = db.Column(db.Float, nullable=False, default=0.0)
    total_deductions = db.Column(db.Float, nullable=False, default=0.0)
    total_bonuses = db.Column(db.Float, nullable=False, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def total_employees_count(self):
        return self.total_employees

    @property
    def total_payrolls_count(self):
        return self.total_payrolls

    @property
    def total_salaries_paid_amount(self):
        return self.total_salaries_paid

    @property
    def total_deductions_amount(self):
        return self.total_deductions

    @property
    def total_bonuses_amount(self):
        return self.total_bonuses
