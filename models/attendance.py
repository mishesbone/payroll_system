from datetime import datetime
from app import db

class Attendance(db.Model):
    __tablename__ = 'attendances'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    check_in = db.Column(db.DateTime, nullable=True)
    check_out = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='present')  # present, absent, late, half_day
    working_hours = db.Column(db.Float, default=0.0)
    overtime_hours = db.Column(db.Float, default=0.0)
    remarks = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    
    # Relationship
    employee = db.relationship('Employee', back_populates='attendances')
    
    def __repr__(self):
        return f'<Attendance {self.employee.employee_id} - {self.date}>'
    
    def __str__(self):
        return f'{self.employee.employee_id} - {self.date}'
    
    @property
    def total_hours(self):
        return self.working_hours + self.overtime_hours
    
    @property
    def is_late(self):
        return self.status == 'late'
    
    @property
    def is_absent(self):
        return self.status == 'absent'
    
    @property
    def is_present(self):
        return self.status == 'present'
    
    @property
    def is_half_day(self):
        return self.status == 'half_day'
    
    @property
    def is_overtime(self):
        return self.overtime_hours > 0.0
    
    @property
    def is_check_in(self):
        return self.check_in is not None
    
    @property
    def is_check_out(self):
        return self.check_out is not None
    
    @property
    def is_weekend(self):
        return self.date.weekday() in [5, 6]
    
    @property
    def is_holiday(self):
        return False
    
    @property
    def is_leave(self):
        return False
    
    @property
    def is_working_day(self):
        return not self.is_weekend and not self.is_holiday and not self.is_leave
    
    @property
    def is_working_hours_valid(self):
        return self.working_hours >= 0.0
    
    @property
    def is_overtime_hours_valid(self):
        return self.overtime_hours >= 0.0
    
    @property
    def is_working_hours_exceeded(self):
        return self.working_hours > 8.0
    
    @property
    def is_overtime_hours_exceeded(self):
        return self.overtime_hours > 0.0
    
    @property
    def is_working_hours_negative(self):
        return self.working_hours < 0.0
    
    @property
    def is_overtime_hours_negative(self):
        return self.overtime_hours < 0.0
    
    