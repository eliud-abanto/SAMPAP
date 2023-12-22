from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Length, Regexp

class EmployeeForm(FlaskForm):
    p00 = StringField(render_kw={"placeholder":"Cédula"}, validators=[DataRequired(message="Ingresa la cédula"), Length(min=1,max=8, message="La cédula debe tener entre 1 y 8 caracteres"),Regexp(r'^\d+$',message='Ingresar solo números')])
    fullname = StringField(render_kw={"placeholder":"Nombre"}, validators=[DataRequired(message="Ingresa tu nombre"), Length(min=4, message="Mínimo 4 caracteres para el nombre"),Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚäëïöüÄËÏÖÜàèìòùÀÈÌÒÙ\s]+$',message='Ingresar solo letras')])
    birthdate = StringField(render_kw={"placeholder":"Fecha de Nacimiento"}, validators=[DataRequired(message="Ingresa la fecha de nacimiento")])
    management = SelectField(u'Elegir Materia', choices=[('Ingeniería en Informática')], validators=[DataRequired(message="Ingresa la carrera")])
    status = StringField('Estado', validators=[DataRequired(message='Ingrese el status')])