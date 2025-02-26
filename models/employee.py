from datetime import datetime
from app import db
from .payroll import Payroll  
from .attendance import Attendance
from .leave import Leave
from .user import User
from models.company import Company



class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    hire_date = db.Column(db.Date, nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    emergency_contact_name = db.Column(db.String(100), nullable=True)
    emergency_contact_phone = db.Column(db.String(20), nullable=True)
    bank_name = db.Column(db.String(100), nullable=True)
    bank_account = db.Column(db.String(50), nullable=True)
    tax_id = db.Column(db.String(50), nullable=True)
    base_salary = db.Column(db.Float, default=0.0)
    employment_status = db.Column(db.String(20), default='active')  # active, terminated, suspended
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    
    # Relationships
    user = db.relationship('User', back_populates='employee')
    payrolls = db.relationship('Payroll', back_populates='employee')
    attendances = db.relationship('Attendance', back_populates='employee')
    leaves = db.relationship('Leave', back_populates='employee')

    
    def __repr__(self):
        return f'<Employee {self.employee_id}>'

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
