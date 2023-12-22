from utils.db import db

class Galery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    def __init__(self, image, description):
        self.image = image
        self.description = description
    
    def to_dict(self):
        return {
            'id': self.id,
            'image': self.image,
            'description': self.description
        }
