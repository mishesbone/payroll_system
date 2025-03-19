# models/deduction.py
from app import db

class Deduction(db.Model):
    __tablename__ = 'deductions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relationships
    company = db.relationship('Company', backref=db.backref('deductions', lazy=True))
    employee = db.relationship('Employee', backref=db.backref('deductions', lazy=True))

    def __repr__(self):
        return f"<Deduction {self.name}, Amount: {self.amount}>"
