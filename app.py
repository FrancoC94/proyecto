from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

from conexion.conexion import conectar
from services.producto_service import (
    obtener_productos,
    insertar_producto,
    eliminar_producto
)
from forms.producto_form import ProductoForm
from reportlab.platypus import SimpleDocTemplate, Table
import os

app = Flask(__name__)
app.secret_key = "secreto123"

# 🔐 CONFIGURACIÓN DE LOGIN
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# 🔐 CLASE USUARIO
class Usuario(UserMixin):
    def __init__(self, id, nombre, email):
        self.id = str(id)
        self.nombre = nombre
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    conn = conectar()
    try:
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario=%s", (user_id,))
        user = cursor.fetchone()
        if user:
            return Usuario(user['id_usuario'], user['nombre'], user['email'])
    finally:
        cursor.close()
        conn.close()
    return None

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = conectar()
        try:
            cursor = conn.cursor(dictionary=True, buffered=True)
            cursor.execute("SELECT * FROM usuarios WHERE email=%s AND password=%s", (email, password))
            user = cursor.fetchone()
            if user:
                usuario = Usuario(user['id_usuario'], user['nombre'], user['email'])
                login_user(usuario)
                return redirect(url_for('inicio'))
            else:
                return "❌ Usuario o contraseña incorrectos"
        finally:
            cursor.close()
            conn.close()
    return render_template('login.html')

# ---------------- INICIO (VER DATOS) ----------------
@app.route('/')
@login_required
def inicio():
    productos = obtener_productos()
    conn = conectar()
    try:
        cursor = conn.cursor(dictionary=True, buffered=True)
        
        # Obtener clientes
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()

        # Obtener reservas con JOIN
        cursor.execute("""
            SELECT r.id_reserva, c.nombre, r.fecha, r.descripcion
            FROM reservas r
            JOIN clientes c ON r.cliente_id = c.id_cliente
        """)
        reservas = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    return render_template('index.html', productos=productos, clientes=clientes, reservas=reservas)

# ---------------- CLIENTES (GUARDAR Y ELIMINAR) ----------------
@app.route('/guardar_cliente', methods=['POST'])
@login_required
def guardar_cliente():
    nombre = request.form['nombre']
    email = request.form['email']
    telefono = request.form['telefono']
    
    conn = conectar()
    try:
        cursor = conn.cursor(buffered=True)
        cursor.execute(
            "INSERT INTO clientes (nombre, email, telefono) VALUES (%s, %s, %s)",
            (nombre, email, telefono)
        )
        conn.commit()
    except Exception as e:
        print(f"Error al guardar cliente: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('inicio'))

@app.route('/eliminar_cliente/<int:id>')
@login_required
def eliminar_cliente(id):
    conn = conectar()
    try:
        cursor = conn.cursor(buffered=True)
        cursor.execute("DELETE FROM clientes WHERE id_cliente=%s", (id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('inicio'))

# ---------------- RESERVAS (GUARDAR Y ELIMINAR) ----------------
@app.route('/guardar_reserva', methods=['POST'])
@login_required
def guardar_reserva():
    cliente_id = request.form['cliente_id']
    fecha = request.form['fecha']
    descripcion = request.form['descripcion']
    
    conn = conectar()
    try:
        cursor = conn.cursor(buffered=True)
        cursor.execute(
            "INSERT INTO reservas (cliente_id, fecha, descripcion) VALUES (%s, %s, %s)",
            (cliente_id, fecha, descripcion)
        )
        conn.commit()
    except Exception as e:
        print(f"Error al guardar reserva: {e}")
        conn.rollback()
        return f"Error: Asegúrate de que el ID de cliente {cliente_id} existe."
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('inicio'))

@app.route('/eliminar_reserva/<int:id>')
@login_required
def eliminar_reserva(id):
    conn = conectar()
    try:
        cursor = conn.cursor(buffered=True)
        cursor.execute("DELETE FROM reservas WHERE id_reserva=%s", (id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('inicio'))

# ---------------- PRODUCTOS ----------------
@app.route('/guardar', methods=['POST'])
@login_required
def guardar():
    form = ProductoForm(request.form)
    if form.valido():
        insertar_producto(form.nombre, form.precio, form.cantidad)
    return redirect(url_for('inicio'))

@app.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    eliminar_producto(id)
    return redirect(url_for('inicio'))

# ---------------- OTROS ----------------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/reporte')
@login_required
def reporte():
    ruta_pdf = os.path.join(os.getcwd(), "reporte.pdf")
    productos = obtener_productos()
    pdf = SimpleDocTemplate(ruta_pdf)
    datos = [["ID", "Nombre", "Precio", "Cantidad"]]
    for p in productos:
        datos.append([p['id'], p['nombre'], p['precio'], p['cantidad']])
    tabla = Table(datos)
    pdf.build([tabla])
    return send_file(ruta_pdf, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)