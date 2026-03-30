from conexion.conexion import conectar

def obtener_productos():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    datos = cursor.fetchall()
    conn.close()
    return datos


def insertar_producto(nombre, precio, cantidad):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO productos (nombre, precio, cantidad) VALUES (%s, %s, %s)",
        (nombre, precio, cantidad)
    )
    conn.commit()
    conn.close()


def eliminar_producto(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id=%s", (id,))
    conn.commit()
    conn.close()