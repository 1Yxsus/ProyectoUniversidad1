from app.utils.database import DatabaseConnection

class AulaUsuarioModel:
    def __init__(self):
        self.db = DatabaseConnection()

    def create(self, id_aula, id_usuario, rol="ALUMNO"):
        query = "INSERT INTO aulas_usuarios (id_aula, id_usuario, rol) VALUES (%s, %s, %s)"
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(query, (id_aula, id_usuario, rol))
        conn.commit()
        conn.close()

    def get_by_aula(self, id_aula):
        query = """SELECT au.*, u.nombre, u.apellido, u.correo 
                   FROM aulas_usuarios au
                   JOIN usuarios u ON au.id_usuario = u.id_usuario
                   WHERE au.id_aula = %s"""
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (id_aula,))
        result = cursor.fetchall()
        conn.close()
        return result

    def update_rol(self, id_aula_usuario, rol):
        query = "UPDATE aulas_usuarios SET rol=%s WHERE id_aula_usuario=%s"
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(query, (rol, id_aula_usuario))
        conn.commit()
        conn.close()

    def delete(self, id_aula_usuario):
        query = "DELETE FROM aulas_usuarios WHERE id_aula_usuario=%s"
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(query, (id_aula_usuario,))
        conn.commit()
        conn.close()
