from app import db
from datetime import datetime

class Holiday(db.Model):
    __tablename__ = 'holidays'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Holiday {self.name} - {self.date}>'
    
    def __str__(self):
        return f'{self.name} - {self.date}'
    
    @property
    def is_upcoming(self):
        return self.date > datetime.now().date()
    
    @property
    def is_past(self):
        return self.date < datetime.now().date()
    
    @property
    def is_today(self):
        return self.date == datetime.now().date()
    
    @property
    def is_weekend(self):
        return self.date.weekday() in [5, 6]
    
    @property
    def day_name(self):
        return self.date.strftime('%A')
    
    @property
    def month_name(self):
        return self.date.strftime('%B')
    
    @property
    def year(self):
        return self.date.year

class HolidayType(db.Model):
    __tablename__ = 'holiday_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<HolidayType {self.name}>'
    
    def __str__(self):
        return self.name