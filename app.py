from flask import Flask, render_template, request, redirect
import json
import csv

from inventario.bd import Producto, db

app = Flask(__name__)

# CONFIGURACIÓN BASE DE DATOS
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///productos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# ---------------- RUTA PRINCIPAL ----------------
@app.route('/')
def inicio():
    return render_template('index.html')

# ---------------- GUARDAR DATOS ----------------
@app.route('/guardar', methods=['POST'])
def guardar():

    nombre = request.form['nombre']
    precio = request.form['precio']
    cantidad = request.form['cantidad']

    # TXT
    with open('inventario/data/datos.txt', 'a') as f:
        f.write(nombre + "," + precio + "," + cantidad + "\n")

    # JSON
    data = {
        "nombre": nombre,
        "precio": precio,
        "cantidad": cantidad
    }

    try:
        with open('inventario/data/datos.json', 'r') as f:
            datos = json.load(f)
    except:
        datos = []

    datos.append(data)

    with open('inventario/data/datos.json', 'w') as f:
        json.dump(datos, f, indent=4)

    # CSV
    with open('inventario/data/datos.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([nombre, precio, cantidad])

    # BASE DE DATOS
    nuevo = Producto(nombre=nombre, precio=precio, cantidad=cantidad)
    db.session.add(nuevo)
    db.session.commit()

    return redirect('/')

# ---------------- VER DATOS ----------------
@app.route('/datos')
def datos():

    with open('inventario/data/datos.txt', 'r') as f:
        datos_txt = f.readlines()

    with open('inventario/data/datos.json', 'r') as f:
        datos_json = json.load(f)

    with open('inventario/data/datos.csv', 'r') as f:
        reader = csv.reader(f)
        datos_csv = list(reader)

    productos = Producto.query.all()

    return render_template(
        'datos.html',
        txt=datos_txt,
        json=datos_json,
        csv=datos_csv,
        productos=productos
    )

# ---------------- EJECUTAR ----------------
if __name__ == '__main__':
    app.run(debug=True)