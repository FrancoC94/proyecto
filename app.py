from flask import Flask, render_template

app = Flask(__name__)

# Ruta principal
@app.route('/')
def inicio():
    return render_template('index.html')

# Ruta acerca de
@app.route('/about')
def about():
    return render_template('about.html')

# Ruta dinámica usuario
@app.route('/usuario/<nombre>')
def usuario(nombre):
    return render_template('index.html', nombre=nombre)

# Ruta dinámica producto
@app.route('/producto/<nombre>')
def producto(nombre):
    return f'Producto: {nombre} – disponible en tienda'

if __name__ == '__main__':
    app.run(debug=True)