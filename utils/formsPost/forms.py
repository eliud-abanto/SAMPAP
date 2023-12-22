from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError, Optional, ValidationError, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired
from models.post import Post


class PostForm(FlaskForm):
    title = StringField('Titulo', validators=[DataRequired(message='Ingrese el titulo')])
    description = StringField('Descripcion', validators =[DataRequired(message='Ingrese una descripcion'), Length(max=50, message="Máximo 50 caracteres para la descripción")])
    image = FileField('Imagen', validators=[Optional(),FileRequired(message="El archivo es requerida"),FileAllowed(['xlsx', 'xls', 'doc', 'docx'], 'Por favor subir solo achivos con el formato permitido')])
    def validate_image(self, image):
        user = Post.query.filter_by(image=image.data).first()
        if user is not None:
            raise ValidationError('El archivo ya existe')
    status = StringField('Estado', validators=[DataRequired(message='¿Cual es el estado del archivo?')])