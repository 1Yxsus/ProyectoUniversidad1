from app.utils.database import get_connection
import re

def authenticate_user(correo, password):
    # conn = get_connection()
    # cur = conn.cursor()
    # # CORREGIDO: MySQL usa %s en lugar de ?
    # cur.execute("SELECT * FROM usuarios WHERE correo=%s AND contrasena=%s", (correo, password))
    # user = cur.fetchone()
    # conn.close()
    # return user

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT id_usuario, nombre, apellido, correo, fecha_registro
        FROM usuarios
        WHERE correo = %s AND contrasena = %s
    """
    cursor.execute(query, (correo, password))
    user = cursor.fetchone()

    cursor.close()
    conn.close()
    return user


# def register_user(nombre, apellido, correo, contrasena):
#     # Validaciones básicas
#     if not nombre or not apellido:
#         raise ValueError("Nombre y apellido son obligatorios.")
#     correo = (correo or "").strip().lower()
#     if not correo or not re.match(r"^[^@]+@[^@]+\.[^@]+$", correo):
#         raise ValueError("Correo inválido.")
#     if not contrasena or len(contrasena) < 8:
#         raise ValueError("La contraseña debe tener al menos 8 caracteres.")
    
#     db = get_connection()
#     cursor = db.cursor()

#     cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
#     if cursor.fetchone():
#         mensaje_error.value = "⚠ El correo ya está registrado"
#         page.update()
#         cursor.close()
#         db.close()
#         return

#     cursor.execute("""
#         INSERT INTO usuario (nombre, apellido, correo, contraseña)
#         VALUES (%s, %s, %s, %s)
#     """, (nombre, apellido, correo, contrasena))
#     db.commit()
#     cursor.close()
#     db.close()

def register_user(nombre: str, apellido: str, correo: str, contrasena: str):
    """
    Intenta registrar un usuario.
    Devuelve (True, None) si tuvo éxito.
    Devuelve (False, "mensaje") en caso de error o si el correo ya existe.
    """
    db = None
    cursor = None
    try:
        db = get_connection()
        cursor = db.cursor()

        # Verificar si ya existe el correo
        cursor.execute("SELECT 1 FROM usuarios WHERE correo = %s", (correo,))
        if cursor.fetchone():
            return False, "El correo ya está registrado"

        # Insertar usuario (ajusta nombre de tabla/columna según tu esquema)
        cursor.execute("""
            INSERT INTO usuarios (nombre, apellido, correo, contrasena)
            VALUES (%s, %s, %s, %s)
        """, (nombre, apellido, correo, contrasena))
        db.commit()
        return True, None

    except Exception as ex:
        if db:
            try:
                db.rollback()
            except Exception:
                pass
        # opcional: registrar traceback en logs
        return False, str(ex)
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()