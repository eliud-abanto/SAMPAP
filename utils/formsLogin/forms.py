from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Optional, Regexp, ValidationError
from models.user import User

class LoginForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired(message="Ingresa el usuario")])
    password = PasswordField("Contraseña", validators=[DataRequired(message="Ingresa la contraseña")])
 
class SignUpForm(FlaskForm):
    firstname = StringField(render_kw={"placeholder":"Nombre"}, validators=[DataRequired(message="Ingresa tu nombre"), Length(min=4, message="Minimo 4 caracteres para el nombre"),Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚäëïöüÄËÏÖÜàèìòùÀÈÌÒÙ\s]+$',message='Ingresar solo letras')])
    lastname = StringField(render_kw={"placeholder":"Apellido"}, validators=[DataRequired(message="Ingresa tu apellido"), Length(min=4, message="Minimo 4 caracteres para el apellido"),Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚäëïöüÄËÏÖÜàèìòùÀÈÌÒÙ\s]+$',message='Ingresar solo letras')])
    username = StringField(render_kw={"placeholder":"Usuario"}, validators=[DataRequired(message="Ingresa tu usuario"), Length(min=4, message="Minimo 4 caracteres para el usuario")])
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('El nombre de usuario ya existe')
    #password = PasswordField(render_kw={"placeholder":"Contraseña"}, validators=[Optional(),Length(min=4, message="Minimo 4 caracteres para la clave"),Regexp(r'^[A-Z][a-zA-Z0-9,!,*,#,$,@]+$',message='Contraseña posee caracteres invalidos')])
    password = PasswordField(render_kw={"placeholder":"Contraseña"}, validators=[Optional(),Length(min=4, message="Minimo 4 caracteres para la clave")])
    #password = PasswordField(render_kw={"placeholder":"Contraseña"}, validators=[Optional(),DataRequired(message="Ingresa tu contraseña"), Length(min=4, message="Minimo 4 caracteres para la clave")])
    role = SelectField(u'Elegir Rol', choices=[('Admin', 'Admin'), ('Estudiante', 'Estudiante')], validators=[DataRequired(message="Ingresa un rol")])
    status = SelectField(u'Elegir Status', choices=[('1', 'Activo'), ('0', 'Inactivo')], validators=[DataRequired(message="Ingresa un status")])