#models/paycode.py
from app import db

class Paycode(db.Model):
    __tablename__ = 'paycodes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relationships
    company = db.relationship('Company', backref=db.backref('paycodes', lazy=True))

    def __repr__(self):
        return f"<Paycode {self.name}, Code: {self.code}>"

    def __str__(self):
        return self.name
    