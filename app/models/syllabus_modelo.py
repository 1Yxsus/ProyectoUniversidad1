from app.utils.database import DatabaseConnection

class SyllabusModel:
    def __init__(self):
        self.db = DatabaseConnection()

    # ----------------------------------------
    # CREATE
    # ----------------------------------------
    def create(self, id_curso, texto_syllabus):
        """
        Inserta un nuevo texto de syllabus asociado a un curso.
        """
        query = """
        INSERT INTO syllabus_texto (id_curso, texto_syllabus)
        VALUES (%s, %s)
        """
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(query, (id_curso, texto_syllabus))
        conn.commit()
        conn.close()
        return True

    # ----------------------------------------
    # READ
    # ----------------------------------------
    def get_by_curso(self, id_curso):
        """
        Obtiene el texto del syllabus de un curso específico.
        """
        query = """
        SELECT id_syllabus, id_curso, texto_syllabus, fecha_registro
        FROM syllabus_texto
        WHERE id_curso = %s
        """
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (id_curso,))
        result = cursor.fetchone()
        conn.close()
        return result

    def get_all(self):
        """
        Obtiene todos los registros de syllabus.
        """
        query = "SELECT * FROM syllabus_texto ORDER BY fecha_registro DESC"
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return result

    # ----------------------------------------
    # UPDATE
    # ----------------------------------------
    def update(self, id_syllabus, nuevo_texto):
        """
        Actualiza el texto del syllabus.
        """
        query = "UPDATE syllabus_texto SET texto_syllabus = %s WHERE id_syllabus = %s"
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(query, (nuevo_texto, id_syllabus))
        conn.commit()
        conn.close()
        return True
    
    def update_by_curso(self, id_curso, texto):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE syllabus_texto SET texto_syllabus = %s WHERE id_curso = %s", (texto, id_curso))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    # ----------------------------------------
    # DELETE
    # ----------------------------------------
    def delete(self, id_syllabus):
        """
        Elimina un registro de syllabus por su ID.
        """
        query = "DELETE FROM syllabus_texto WHERE id_syllabus = %s"
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(query, (id_syllabus,))
        conn.commit()
        conn.close()
        return True
