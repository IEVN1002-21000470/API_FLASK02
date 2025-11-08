from wtforms import Form
from wtforms import StringField, PasswordField, EmailField, BooleanField, SubmitField, IntegerField
from wtforms import validators

class UserForm(Form):
    matricula= IntegerField("Matricula", [
        validators.DataRequired(message='El campo es requerido')
    ])
    nombre=StringField('Nombre',[
        validators.DataRequired(message='El campo es requerido')
    ])
    apellido=StringField("Apellido",[
        validators.DataRequired(message='El campo es requerido')
    ])
    correo=EmailField("Correo",[
    validators.Email(message='Ingrese Correo valido')
    ])

class PizzeriaForm(Form):
    nombre_cliente = StringField('Nombre', [
        validators.DataRequired(message='El campo es requerido')
    ])
    direccion = StringField('Direccion', [
        validators.DataRequired(message='El campo es requerido')
    ])
    telefono = StringField('Telefono', [
        validators.DataRequired(message='El campo es requerido')
    ])
    fecha = StringField('Fecha', [
        validators.DataRequired(message='El campo es requerido')
    ])
    tamano = StringField('Tamano', [
        validators.DataRequired(message='Seleccione un tamaño')
    ])
    ingredientes = StringField('Ingredientes')
    numero_pizzas = IntegerField('Numero de Pizzas', [
        validators.DataRequired(message='El campo es requerido'),
        validators.NumberRange(min=1, message='Debe ser al menos 1')
    ])
