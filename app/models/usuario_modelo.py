from app.utils.database import DatabaseConnection

class UsuarioModel:
    def __init__(self):
        self.db = DatabaseConnection()

    def create(self, nombre, apellido, correo, contrasena):
        query = "INSERT INTO usuarios (nombre, apellido, correo, contrasena) VALUES (%s, %s, %s, %s)"
        params = (nombre, apellido, correo, contrasena)
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()

    def get_all(self):
        query = "SELECT * FROM usuarios"
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return result

    def get_by_id(self, id_usuario):
        query = "SELECT * FROM usuarios WHERE id_usuario = %s"
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (id_usuario,))
        result = cursor.fetchone()
        conn.close()
        return result
    
    def get_by_credentials(self, correo, contrasena):
        """
        Obtiene el usuario por su correo y contraseña (texto plano)
        """
        query = "SELECT * FROM usuarios WHERE correo = %s AND contrasena = %s"
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (correo, contrasena))
        result = cursor.fetchone()
        conn.close()
        return result


    def update(self, id_usuario, nombre, apellido, correo):
        query = "UPDATE usuarios SET nombre=%s, apellido=%s, correo=%s WHERE id_usuario=%s"
        params = (nombre, apellido, correo, id_usuario)
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()

    def delete(self, id_usuario):
        query = "DELETE FROM usuarios WHERE id_usuario = %s"
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(query, (id_usuario,))
        conn.commit()
        conn.close()
