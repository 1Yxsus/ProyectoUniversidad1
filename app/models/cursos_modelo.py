from app.utils.database import DatabaseConnection

class CursoModel:
    def __init__(self):
        self.db = DatabaseConnection()

    def create(self, id_aula, nombre_curso, descripcion, id_delegado=None):
        query = "INSERT INTO cursos (id_aula, nombre_curso, descripcion, id_delegado) VALUES (%s, %s, %s, %s)"
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(query, (id_aula, nombre_curso, descripcion, id_delegado))
        conn.commit()
        conn.close()

    def get_by_aula(self, id_aula):
        query = "SELECT * FROM cursos WHERE id_aula = %s"
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (id_aula,))
        result = cursor.fetchall()
        conn.close()
        return result
    
    def get_by_usuario(self, id_usuario):
        """
        Obtiene todos los cursos a los que el usuario tiene acceso,
        según las aulas a las que pertenece.
        """
        query = """
        SELECT 
            c.id_curso,
            c.nombre_curso,
            c.descripcion,
            c.id_aula,
            a.nombre_aula,
            au.rol
        FROM cursos c
        JOIN aulas a ON c.id_aula = a.id_aula
        JOIN aulas_usuarios au ON a.id_aula = au.id_aula
        WHERE au.id_usuario = %s
        ORDER BY a.nombre_aula, c.nombre_curso
        """
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (id_usuario,))
        result = cursor.fetchall()
        conn.close()
        return result
    
    def get_by_aula(self, id_aula):
        """
        Obtiene todos los cursos que pertenecen a un aula específica.
        """
        query = """
        SELECT 
            c.id_curso,
            c.nombre_curso,
            c.descripcion,
            c.id_aula,
            a.nombre_aula,
            u.nombre AS delegado_nombre,
            u.apellido AS delegado_apellido
        FROM cursos c
        JOIN aulas a ON c.id_aula = a.id_aula
        LEFT JOIN usuarios u ON c.id_delegado = u.id_usuario
        WHERE c.id_aula = %s
        ORDER BY c.fecha_creacion DESC
        """
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (id_aula,))
        result = cursor.fetchall()
        conn.close()
        return result

    def update(self, id_curso, nombre_curso, descripcion):
        query = "UPDATE cursos SET nombre_curso=%s, descripcion=%s WHERE id_curso=%s"
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(query, (nombre_curso, descripcion, id_curso))
        conn.commit()
        conn.close()

    def delete(self, id_curso):
        query = "DELETE FROM cursos WHERE id_curso=%s"
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(query, (id_curso,))
        conn.commit()
        conn.close()
