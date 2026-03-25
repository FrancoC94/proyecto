from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

from conexion.conexion import conectar

app = Flask(__name__)
app.secret_key = "secreto123"

# 🔐 LOGIN
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# 🔐 USUARIO
class Usuario(UserMixin):
    def __init__(self, id, nombre, email):
        self.id = str(id)
        self.nombre = nombre
        self.email = email


@login_manager.user_loader
def load_user(user_id):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE id_usuario=%s", (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return Usuario(user['id_usuario'], user['nombre'], user['email'])
    return None


# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM usuarios WHERE email=%s AND password=%s",
            (email, password)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            usuario = Usuario(user['id_usuario'], user['nombre'], user['email'])
            login_user(usuario)
            return redirect(url_for('inicio'))
        else:
            return "❌ Usuario incorrecto"

    return render_template('login.html')


# ---------------- REGISTRO ----------------
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
            (nombre, email, password)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/login')

    return render_template('registro.html')


# ---------------- LOGOUT ----------------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


# ---------------- INICIO ----------------
@app.route('/')
@login_required
def inicio():
    conn = conectar()

    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        cursor.close()
        conn.close()
    else:
        productos = []

    return render_template('index.html', productos=productos)


# ---------------- PRODUCTOS ----------------
@app.route('/guardar', methods=['POST'])
@login_required
def guardar():
    nombre = request.form['nombre']
    precio = request.form['precio']
    cantidad = request.form['cantidad']

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


@app.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    conn = conectar()

    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()

    return redirect('/')


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    conn = conectar()

    if request.method == 'POST':
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE productos SET nombre=%s, precio=%s, cantidad=%s WHERE id=%s",
            (request.form['nombre'], request.form['precio'], request.form['cantidad'], id)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/')

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id=%s", (id,))
    producto = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('editar.html', producto=producto)


# ---------------- CLIENTES ----------------
@app.route('/clientes')
@login_required
def clientes():
    conn = conectar()
    clientes = []

    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()
        cursor.close()
        conn.close()

    return render_template('clientes.html', clientes=clientes)


@app.route('/guardar_cliente', methods=['POST'])
@login_required
def guardar_cliente():
    nombre = request.form['nombre']
    email = request.form['email']
    telefono = request.form['telefono']

    conn = conectar()

    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clientes (nombre, email, telefono) VALUES (%s, %s, %s)",
            (nombre, email, telefono)
        )
        conn.commit()
        cursor.close()
        conn.close()

    return redirect('/clientes')


@app.route('/eliminar_cliente/<int:id>')
@login_required
def eliminar_cliente(id):
    conn = conectar()

    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE id_cliente=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()

    return redirect('/clientes')


# ---------------- RESERVAS ----------------
@app.route('/reservas')
@login_required
def reservas():
    conn = conectar()
    reservas = []

    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT r.id_reserva, c.nombre, r.fecha, r.descripcion
            FROM reservas r
            JOIN clientes c ON r.cliente_id = c.id_cliente
        """)
        reservas = cursor.fetchall()
        cursor.close()
        conn.close()

    return render_template('reservas.html', reservas=reservas)


@app.route('/guardar_reserva', methods=['POST'])
@login_required
def guardar_reserva():
    cliente_id = request.form['cliente_id']
    fecha = request.form['fecha']
    descripcion = request.form['descripcion']

    conn = conectar()

    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reservas (cliente_id, fecha, descripcion) VALUES (%s, %s, %s)",
            (cliente_id, fecha, descripcion)
        )
        conn.commit()
        cursor.close()
        conn.close()

    return redirect('/reservas')


@app.route('/eliminar_reserva/<int:id>')
@login_required
def eliminar_reserva(id):
    conn = conectar()

    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reservas WHERE id_reserva=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()

    return redirect('/reservas')


# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)