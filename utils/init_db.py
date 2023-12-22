from utils.db import db
from models.user import User

def create_user_default():
    default_user = User(
        firstname='Default',
        lastname='User',
        username='defaultadmin',
        password='12345678',
        role='Admin',
        status=1
    )
    db.session.add(default_user)
    db.session.commit()