import os

def conectar():
    # 👉 En Render NO usamos MySQL
    if os.environ.get("RENDER"):
        return None

    # 👉 En tu PC sí usa MySQL
    import mysql.connector

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="tienda"
    )