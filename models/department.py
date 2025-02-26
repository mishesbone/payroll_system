#models/departments.py
from app import db
from datetime import datetime
from models.employee import Employee

class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    employees = db.relationship('Employee', back_populates='department')


    
    def __repr__(self):
        return f'<Department {self.name}>'
    
    @property
    def total_employees(self):
        return len(self.employees)
    
    