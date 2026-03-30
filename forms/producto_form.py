class ProductoForm:
    def __init__(self, form):
        self.nombre = form.get("nombre")
        self.precio = form.get("precio")
        self.cantidad = form.get("cantidad")

    def valido(self):
        return self.nombre != "" and self.precio != "" and self.cantidad != ""