from app import db

class UserCompany(db.Model):
    __tablename__ = 'user_companies'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('user_companies', lazy=True))
    company = db.relationship('Company', backref=db.backref('user_companies', lazy=True))
