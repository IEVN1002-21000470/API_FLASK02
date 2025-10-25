from flask import Flask, render_template, render_template, request
import math as mt
import forms

app = Flask(__name__)


@app.route("/index")
def home():
    titulo = "Pagina de inicio"
    listado = ["Pthon", "Flask", "Jinja2", "html", "css"]
    return render_template("index.html", titulo=titulo, listado=listado)


@app.route("/calculos", methods=["GET", "POST"])
def about():
    if request.method == "POST":
        numero1 = request.form["numero1"]
        numero2 = request.form["numero2"]
        opcin = request.form["operacion"]
        if opcin == "suma":
            res = int(numero1) + int(numero2)
        if opcin == "resta":
            res = int(numero1) - int(numero2)
        if opcin == "multiplicacion":
            res = int(numero1) * int(numero2)
        if opcin == 'division':
            res = int(numero1) / int(numero2)

        return render_template("calculos.html", res=res, numero1=numero1, numero2=numero2)
    return render_template("calculos.html")


@app.route("/distancia", methods =["GET", "POST"])
def distancia():
    if request.method == "POST":
        x1 = float(request.form["x1"])
        y1 = float(request.form["y1"])
        x2 = float(request.form["x2"])
        y2 = float(request.form["y2"])
        distancia = mt.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return render_template("distancia.html", distancia=distancia, x1=x1, y1=y1, x2=x2, y2=y2)
    return render_template("distancia.html", distancia=None)


@app.route("/user/<string:user>")
def user(user):
    return f"Hola, {user}!"


@app.route("/numero/<int:num>")
def func(num):
    return f"El numero es: {num}"


@app.route("/suma/<int:num1>/<int:num2>")
def suma(num1, num2):
    return f"La suma es: {num1 + num2}"


@app.route("/user/<int:id>/<string:username>")
def username(id, username):
    return "ID: {} nombre: {}".format(id, username)


@app.route("/suma/<float:n1>/<float:n2>")
def func1(n1, n2):
    return "la suma es: {}".format(n1 + n2)


@app.route("/default/")
@app.route("/default/<string:dft>")
def func2(dft="sss"):
    return "El valor de dft es: " + dft

@app.route("/Alumnos", methods=['GET', 'POST'])
def alumnos():
    mat=0
    nom=""
    ape=""
    email=""
    alumno_clas=forms.UserForm(request.form)
    if request.method =="POST" and alumno_clas.validate():
        mat=alumno_clas.matricula.data
        nom=alumno_clas.nombre.data
        ape=alumno_clas.apellido.data
        email=alumno_clas.correo.data
    return render_template('Alumnos.html', form=alumno_clas, mat=mat, nom=nom, ape=ape, email=email)


@app.route("/prueba")
def func4():
    return """
  <html>
    <head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous">
    <title>Pagina de prueba</title>
    </head>
      <body>
        <h1>hola esta es una pagina web</h1>
        <p>Esta es para probar el entorno de trabajo</p>
      </body>
  </html>
  """


if __name__ == "__main__":
    app.run(debug=True)
