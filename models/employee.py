import logging
from datetime import datetime

from sqlalchemy import Column, Integer
from app import db

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='payroll_system.log')
logger = logging.getLogger('employee')

class Employee(db.Model):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    employee_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    hire_date = db.Column(db.Date, nullable=False)
    position = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, default=0.0)

    # Relationships
    paid_activities = db.relationship('PaidActivity', back_populates='employee', cascade='all, delete-orphan')
    provider_rates = db.relationship('ProviderRate', back_populates='employee', cascade='all, delete-orphan')
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def calculate_years_of_service(self):
        """Calculate years of service based on hire date"""
        if not self.hire_date:
            return 0
        
        try:
            today = datetime.now()
            years_of_service = today.year - self.hire_date.year
            
            # Adjust for hire date not yet reached in current year
            if (today.month, today.day) < (self.hire_date.month, self.hire_date.day):
                years_of_service -= 1
                
            return max(0, years_of_service)
        except Exception as e:
            logger.error(f"Error calculating years of service: {e}")
            return 0
    
    def to_dict(self):
        """Convert employee object to dictionary"""
        return {
            'employee_id': self.employee_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'hire_date': self.hire_date.strftime("%Y-%m-%d") if isinstance(self.hire_date, datetime) else self.hire_date,
            'position': self.position,
            'department': self.department,
            'salary': self.salary
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create employee object from dictionary"""
        if not data:
            return None
            
        # Handle hire_date conversion
        hire_date = data.get('hire_date')
        if hire_date and isinstance(hire_date, str):
            try:
                hire_date = datetime.strptime(hire_date, "%Y-%m-%d")
            except ValueError:
                logger.error(f"Invalid date format for hire_date: {hire_date}")
                
        return cls(
            employee_id=data.get('employee_id'),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            email=data.get('email', ''),
            phone=data.get('phone', ''),
            hire_date=hire_date,
            position=data.get('position', ''),
            department=data.get('department', ''),
            salary=data.get('salary', 0.0)
        )
