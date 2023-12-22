from flask import Flask, flash
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask import request, redirect, url_for
from models import Image
from app import app, db, photos

app = Flask(__name__)
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/images'
configure_uploads(app, photos)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'photo' not in request.files:
        flash('No se proporcionó ningún archivo')
        return redirect(request.referrer)
    photo = request.files['photo']
    if photo.filename == '':
        flash('No se proporcionó ningún archivo')
        return redirect(request.referrer)
    filename = photos.save(photo)
    # Crea un nuevo registro en la base de datos con la ruta del archivo
    image = Image(filename=filename)
    db.session.add(image)
    db.session.commit()
    flash('Archivo subido exitosamente')
    return redirect(url_for('index'))

from app import db

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256))