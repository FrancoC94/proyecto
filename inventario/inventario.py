from .productos import Producto

class Inventario:
    def __init__(self):
        self.productos = {}

    def agregar(self, producto):
        self.productos[producto.id] = producto

    def eliminar(self, id):
        if id in self.productos:
            del self.productos[id]

    def actualizar(self, id, precio=None, cantidad=None):
        if id in self.productos:
            if precio:
                self.productos[id].precio = precio
            if cantidad:
                self.productos[id].cantidad = cantidad

    def buscar(self, nombre):
        resultados = []
        for p in self.productos.values():
            if nombre.lower() in p.nombre.lower():
                resultados.append(p)
        return resultados

    def listar(self):
        return self.productos