from utils.db import db
from datetime import datetime

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    p00 = db.Column(db.Integer, nullable=False, unique=True)
    fullname = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.Date)
    management = db.Column(db.String(100))
    status = db.Column(db.Integer, default=1)

    def __init__(self, p00, fullname, birthdate, management, status):
        self.p00 = p00
        self.fullname = fullname
        self.birthdate = birthdate
        self.management = management
        self.status = status
    
    @property
    def birthdate_str(self):
        return self.birthdate.strftime('%d/%m/%Y')
    
    @birthdate_str.setter
    def birthdate_str(self, value):
        self.birthdate = datetime.strptime(value, '%d/%m/%Y')
    
    def to_dict(self):
        return {
            'id': self.id,
            'p00': self.p00,
            'fullname': self.fullname,
            'birthdate': self.birthdate_str,
            'management': self.management,
            'status': self.status
        }

