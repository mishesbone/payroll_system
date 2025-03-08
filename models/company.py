from app import db
from datetime import datetime
from models import Employee, Payroll, User


class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', back_populates='company')
    employees = db.relationship('Employee', back_populates='company')
    payrolls = db.relationship('Payroll', back_populates='company')

    # Delayed Import for PayrollReport to avoid circular imports
    def get_payroll_reports(self):
        from models.payroll import PayrollReport
        return PayrollReport.query.filter_by(company_id=self.id).all()
