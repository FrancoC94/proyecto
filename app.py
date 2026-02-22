from flask import Flask

app = Flask(__name__)

@app.route('/')
def inicio():
    return "Bienvenido a Tienda Online – Catálogo y ofertas"

@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f'Bienvenido, {nombre}!'

@app.route('/producto/<nombre>')
def producto(nombre):
    return f'Producto: {nombre} – disponible en tienda'

if __name__ == '__main__':
    app.run()
