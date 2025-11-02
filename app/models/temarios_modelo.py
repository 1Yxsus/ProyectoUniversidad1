from app.utils.database import DatabaseConnection

class TemarioModel:
    def __init__(self):
        self.db = DatabaseConnection()

    def create(self, id_curso, contenido_generado, fuente="IA"):
        query = """INSERT INTO temarios (id_curso, contenido_generado, fuente)
                   VALUES (%s, %s, %s)"""
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(query, (id_curso, contenido_generado, fuente))
        conn.commit()
        conn.close()

    def get_by_curso(self, id_curso):
        query = "SELECT * FROM temarios WHERE id_curso=%s"
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (id_curso,))
        result = cursor.fetchall()
        conn.close()
        return result

    def delete(self, id_temario):
        query = "DELETE FROM temarios WHERE id_temario=%s"
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(query, (id_temario,))
        conn.commit()
        conn.close()
