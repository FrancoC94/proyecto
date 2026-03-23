from inventario.productos import Producto

class Inventario:
    def __init__(self):
        self.productos = {}

    def agregar(self, producto):
        self.productos[producto.id] = producto

    def eliminar(self, id):
        if id in self.productos:
            del self.productos[id]

    def actualizar(self, id, cantidad=None, precio=None):
        if id in self.productos:
            if cantidad is not None:
                self.productos[id].set_cantidad(cantidad)
            if precio is not None:
                self.productos[id].set_precio(precio)

    def buscar(self, nombre):
        resultados = []
        for p in self.productos.values():
            if nombre.lower() in p.nombre.lower():
                resultados.append(p)
        return resultados

    def listar(self):
        return self.productos