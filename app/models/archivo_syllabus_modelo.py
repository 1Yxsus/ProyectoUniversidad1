from app.utils.database import DatabaseConnection

class ArchivoSyllabusModel:
    def __init__(self):
        self.db = DatabaseConnection()

    def create(self, id_curso, nombre_archivo, ruta_archivo, tipo_archivo, subido_por):
        query = """INSERT INTO archivos_syllabus 
                   (id_curso, nombre_archivo, ruta_archivo, tipo_archivo, subido_por)
                   VALUES (%s, %s, %s, %s, %s)"""
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(query, (id_curso, nombre_archivo, ruta_archivo, tipo_archivo, subido_por))
        conn.commit()
        conn.close()

    def get_by_curso(self, id_curso):
        query = "SELECT * FROM archivos_syllabus WHERE id_curso=%s"
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (id_curso,))
        result = cursor.fetchall()
        conn.close()
        return result

    def delete(self, id_archivo):
        query = "DELETE FROM archivos_syllabus WHERE id_archivo=%s"
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(query, (id_archivo,))
        conn.commit()
        conn.close()
