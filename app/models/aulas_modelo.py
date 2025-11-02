from app.utils.database import DatabaseConnection

class AulaModel:
    def __init__(self):
        self.db = DatabaseConnection()

    def create(self, nombre_aula, descripcion, id_admin):
        query = "INSERT INTO aulas (nombre_aula, descripcion, id_admin) VALUES (%s, %s, %s)"
        params = (nombre_aula, descripcion, id_admin)
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        return cursor.lastrowid

    def get_all(self):
        query = "SELECT * FROM aulas"
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return result

    def get_by_id(self, id_aula):
        query = "SELECT * FROM aulas WHERE id_aula = %s"
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (id_aula,))
        result = cursor.fetchone()
        conn.close()
        return result
    
    def get_last_inserted_id(self):
        query = "SELECT LAST_INSERT_ID() AS last_id"
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    
    def get_by_usuario(self, id_usuario):
        
        #   Obtiene todas las aulas donde el usuario participa (admin, delegado o alumno)
        query = """
        SELECT a.*, au.rol 
        FROM aulas a
        JOIN aulas_usuarios au ON a.id_aula = au.id_aula
        WHERE au.id_usuario = %s
        ORDER BY a.fecha_creacion DESC
        """
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (id_usuario,))
        result = cursor.fetchall()
        conn.close()
        return result

    def update(self, id_aula, nombre_aula, descripcion):
        query = "UPDATE aulas SET nombre_aula=%s, descripcion=%s WHERE id_aula=%s"
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(query, (nombre_aula, descripcion, id_aula))
        conn.commit()
        conn.close()

    def delete(self, id_aula):
        query = "DELETE FROM aulas WHERE id_aula=%s"
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(query, (id_aula,))
        conn.commit()
        conn.close()
