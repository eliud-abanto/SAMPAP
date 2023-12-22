from utils.db import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255))
    role = db.Column(db.String(10), nullable=False)
    status = db.Column(db.Integer, nullable=False)

    def __init__(self, firstname, lastname, username, password, role, status):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role
        self.status = status
    
    # para verificar la contraseña del usuario
    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'username': self.username,
            'role': self.role,
            'status': self.status,
        }
    
    def is_admin(self):
        return self.role == 'Admin'
