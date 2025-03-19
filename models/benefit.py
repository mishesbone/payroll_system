# models/benefit.py
from app import db

class Benefit(db.Model):
    __tablename__ = 'benefits'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    amount = db.Column(db.Float, nullable=False, default=0.0)  # Added amount field
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)  # Linking to employees
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relationships
    company = db.relationship('Company', backref=db.backref('benefits', lazy=True))
    employee = db.relationship('Employee', backref=db.backref('benefits', lazy=True))

    def __repr__(self):
        return f"<Benefit {self.name}, Amount: {self.amount}>"

    def __str__(self):
        return self.name
