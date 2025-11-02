from app.utils.database import DatabaseConnection

class TareaModel:
    def __init__(self):
        self.db = DatabaseConnection()

    def create(self, id_curso, titulo, descripcion, fecha_entrega, publicado_por):
        query = """INSERT INTO tareas (id_curso, titulo, descripcion, fecha_entrega, publicado_por)
                   VALUES (%s, %s, %s, %s, %s)"""
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(query, (id_curso, titulo, descripcion, fecha_entrega, publicado_por))
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
