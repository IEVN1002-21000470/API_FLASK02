from flask import Flask, render_template, render_template, request
from flask import make_response,jsonify,json
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
    tem=[]
    estudiantes=[]
    datos={}

    alumno_clas=forms.UserForm(request.form)
    if request.method =="POST" and alumno_clas.validate():
        if request.form.get("btnElimina")=='eliminar':
            response = make_response(render_template('Alumnos.html',))
            response.delete_cookie('usuario')

        mat=alumno_clas.matricula.data
        nom=alumno_clas.nombre.data
        ape=alumno_clas.apellido.data
        email=alumno_clas.correo.data

        datos={'matricula':mat,'nombre':nom.rstrip(),
               'apellido':ape.rstrip(),'email':email.rstrip()}
        data_str = request.cookies.get("usuario")
        if not data_str:
             return "No hay cookie guardada", 404
        estudiantes = json.loads(data_str)
        estudiantes.append(datos)
    response=make_response(render_template('Alumnos.html',
            form=alumno_clas, mat=mat, nom=nom, apell=ape, email=email))

    if request.method!='GET':
        response.set_cookie('usuario', json.dumps(estudiantes))

    return response


@app.route("/get_cookie")
def get_cookie():
    data_str = request.cookies.get("usuario")
    if not data_str:
        return "No hay cookie guardada", 404
    estudiantes = json.loads(data_str)
    return jsonify(estudiantes)

#*creacion de pizzeria e implementacion de cookies

@app.route("/pizzeria", methods=['GET', 'POST'])
def pizzeria():
    mensaje = ""
    total_pagar = 0
    pedidos = []
    ventas_totales = []

    pizzeria_form = forms.PizzeriaForm(request.form)

    cookie_pedidos = request.cookies.get("pedidos_pizzas")
    if cookie_pedidos:
        pedidos = json.loads(cookie_pedidos)

    cookie_ventas = request.cookies.get("cookie_ventas")
    if cookie_ventas:
        ventas_totales = json.loads(cookie_ventas)

    if request.method == "POST":

        if request.form.get("btnAgregar") == 'agregar' and pizzeria_form.validate():
            ingredientes_list = request.form.getlist('ingredientes')
            ingredientes_str = ', '.join(ingredientes_list) if ingredientes_list else 'Sin ingredientes'

            precios = {'chica': 40,
                       'mediana': 80,
                       'grande': 120}

            precio_base = precios.get(pizzeria_form.tamano.data, 0)
            precio_ingredientes = len(ingredientes_list) * 10
            subtotal = (precio_base + precio_ingredientes) * pizzeria_form.numero_pizzas.data

            pedido = {
                'nombre': pizzeria_form.nombre_cliente.data.rstrip(),
                'direccion': pizzeria_form.direccion.data.rstrip(),
                'telefono': pizzeria_form.telefono.data.rstrip(),
                'fecha': pizzeria_form.fecha.data.rstrip(),
                'tamano': pizzeria_form.tamano.data,
                'ingredientes': ingredientes_str,
                'numero_pizzas': pizzeria_form.numero_pizzas.data,
                'subtotal': subtotal
            }
            pedidos.append(pedido)

        elif request.form.get("btnQuitar") == 'quitar':
            if pedidos:
                pedidos.pop()

        elif request.form.get("btnTerminar") == 'terminar':
            if pedidos:
                total_pagar = sum(p['subtotal'] for p in pedidos)
                mensaje = f"Pedido confirmado. Total a pagar: ${total_pagar}"

                venta = {
                    'nombre': pedidos[0]['nombre'],
                    'direccion': pedidos[0]['direccion'],
                    'telefono': pedidos[0]['telefono'],
                    'fecha': pedidos[0]['fecha'],
                    'total': total_pagar
                }
                ventas_totales.append(venta)

                response = make_response(render_template('pizzeria.html',
                    form=pizzeria_form, pedidos=[], mensaje=mensaje,
                    total_pagar=total_pagar, ventas_totales=ventas_totales))
                response.delete_cookie('pedidos_pizzas')
                response.set_cookie('cookie_ventas', json.dumps(ventas_totales))
                return response

    response = make_response(render_template('pizzeria.html',
        form=pizzeria_form, pedidos=pedidos, mensaje=mensaje,
        total_pagar=total_pagar, ventas_totales=ventas_totales))

    if request.method == 'POST':
        response.set_cookie('pedidos_pizzas', json.dumps(pedidos))

    return response

@app.route("/get_cookie_pizzeria")
def get_cookie_pizzeria():
    data_str = request.cookies.get("pedidos_pizzas")
    if not data_str:
        return "No hay cookie guardada", 404
    pedidos = json.loads(data_str)
    return jsonify(pedidos)

@app.route("/get_cookie_ventas")
def get_cookie_ventas():
    data_str = request.cookies.get("cookie_ventas")
    if not data_str:
        return "No hay cookies guardada", 404
    ventas_totales = json.loads(data_str)
    return jsonify(ventas_totales)

@app.route("/")


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
