from app.utils.database import DatabaseConnection

class TareaModel:
    def __init__(self):
        self.db = DatabaseConnection()

    def create(self, id_aula, id_curso, titulo, descripcion, fecha_entrega, publicado_por):
        query = """INSERT INTO tareas (id_aula, id_curso, titulo, descripcion, fecha_entrega, publicado_por)
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(query, (id_aula, id_curso, titulo, descripcion, fecha_entrega, publicado_por))
        conn.commit()
        conn.close()

    def get_by_curso(self, id_curso):
        query = "SELECT * FROM tareas WHERE id_curso = %s"
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (id_curso,))
        result = cursor.fetchall()
        conn.close()
        return result
    
    
    def get_by_curso_ordenadas(self, id_curso):
        """
        Obtiene todas las tareas de un curso ordenadas por fecha de entrega (más próximas primero).
        """
        query = """
        SELECT 
            id_tarea, 
            titulo, 
            descripcion, 
            fecha_entrega, 
            fecha_publicacion, 
            publicado_por
        FROM tareas
        WHERE id_curso = %s
        ORDER BY fecha_entrega ASC
        """
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (id_curso,))
        result = cursor.fetchall()
        conn.close()
        return result

    def get_by_aula_with_curso(self, id_aula):
        """
        Obtiene todas las tareas de un aula específica,
        mostrando también el nombre del curso asociado.
        """
        query = """
        SELECT 
            t.id_tarea,
            t.id_aula,
            t.id_curso,
            c.nombre_curso,
            t.titulo,
            t.descripcion,
            t.fecha_entrega,
            t.publicado_por,
            t.fecha_publicacion
        FROM tareas t
        JOIN cursos c ON t.id_curso = c.id_curso
        WHERE t.id_aula = %s
        ORDER BY t.fecha_entrega ASC
        """
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (id_aula,))
        result = cursor.fetchall()
        conn.close()
        return result

    def get_all_tareas_by_aula(self, id_aula):
        query = "SELECT * FROM tareas WHERE id_aula = %s ORDER BY fecha_entrega ASC"
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (id_aula,))
        result = cursor.fetchall()
        conn.close()
        return result

    def update(self, id_tarea, titulo, descripcion, fecha_entrega):
        query = "UPDATE tareas SET titulo=%s, descripcion=%s, fecha_entrega=%s WHERE id_tarea=%s"
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(query, (titulo, descripcion, fecha_entrega, id_tarea))
        conn.commit()
        conn.close()

    def delete(self, id_tarea):
        query = "DELETE FROM tareas WHERE id_tarea=%s"
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(query, (id_tarea,))
        conn.commit()
        conn.close()
