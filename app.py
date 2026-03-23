from flask import Flask, render_template, request, redirect
import json
import csv
import os

from conexion.conexion import conectar

app = Flask(__name__)

# ---------------- INICIO ----------------
@app.route('/')
def inicio():
    conn = conectar()

    if conn:  # 👉 LOCAL (MYSQL)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        cursor.close()
        conn.close()
    else:  # 👉 RENDER
        productos = []

    return render_template('index.html', productos=productos)

# ---------------- GUARDAR ----------------
@app.route('/guardar', methods=['POST'])
def guardar():

    nombre = request.form['nombre']
    precio = request.form['precio']
    cantidad = request.form['cantidad']

    # TXT
    with open('inventario/data/datos.txt', 'a') as f:
        f.write(nombre + "," + precio + "," + cantidad + "\n")

    # JSON
    data = {"nombre": nombre, "precio": precio, "cantidad": cantidad}

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

    # MYSQL SOLO LOCAL
    conn = conectar()

    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre, precio, cantidad) VALUES (%s, %s, %s)",
            (nombre, precio, cantidad)
        )
        conn.commit()
        cursor.close()
        conn.close()

    return redirect('/')

# ---------------- ELIMINAR ----------------
@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = conectar()

    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()

    return redirect('/')

# ---------------- EDITAR ----------------
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = conectar()

    if request.method == 'POST':
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE productos SET nombre=%s, precio=%s, cantidad=%s WHERE id=%s",
                (
                    request.form['nombre'],
                    request.form['precio'],
                    request.form['cantidad'],
                    id
                )
            )
            conn.commit()
            cursor.close()
            conn.close()

        return redirect('/')

    producto = None

    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos WHERE id=%s", (id,))
        producto = cursor.fetchone()
        cursor.close()
        conn.close()

    return render_template('editar.html', producto=producto)

# ---------------- BUSCAR ----------------
@app.route('/buscar', methods=['POST'])
def buscar():
    nombre = request.form['nombre']
    conn = conectar()

    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM productos WHERE nombre LIKE %s",
            ('%' + nombre + '%',)
        )
        productos = cursor.fetchall()
        cursor.close()
        conn.close()
    else:
        productos = []

    return render_template('index.html', productos=productos)

# ---------------- DATOS ----------------
@app.route('/datos')
def datos():

    with open('inventario/data/datos.txt', 'r') as f:
        datos_txt = f.readlines()

    with open('inventario/data/datos.json', 'r') as f:
        datos_json = json.load(f)

    with open('inventario/data/datos.csv', 'r') as f:
        reader = csv.reader(f)
        datos_csv = list(reader)

    conn = conectar()

    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        cursor.close()
        conn.close()
    else:
        productos = []

    return render_template(
        'datos.html',
        txt=datos_txt,
        json=datos_json,
        csv=datos_csv,
        productos=productos
    )

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)