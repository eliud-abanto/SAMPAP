from utils.db import db
from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text(50), nullable=False)
    image = db.Column(db.String(100), nullable=True, unique=True)
    slug = db.Column(db.String(200), nullable=False, unique=True)
    status = db.Column(db.Integer, default=1)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='posts')

    def __init__(self, title, description, image, slug, status, date, user_id, created_on, updated_on):
        self.title = title
        self.description = description
        self.image = image
        self.slug = slug
        self.status = status
        self.date = date
        self.user_id = user_id
        if created_on:
            self.created_on = created_on
        if updated_on:
            self.updated_on = updated_on

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image': self.image,
            'slug': self.slug,
            'status': self.status,
        }

