from app.utils.database import DatabaseConnection

class AnunciosModel:
    def __init__(self):
        self.db = DatabaseConnection()

    # ----------------------------------------
    # CREATE
    # ----------------------------------------
    def create(self, id_aula, titulo, descripcion):
        """
        Crea un nuevo anuncio asociado a un aula.
        """
        query = """
        INSERT INTO anuncios (id_aula, titulo, descripcion)
        VALUES (%s, %s, %s)
        """
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(query, (id_aula, titulo, descripcion))
        conn.commit()
        conn.close()
        return True

    # ----------------------------------------
    # READ
    # ----------------------------------------
    def get_by_aula(self, id_aula):
        """
        Obtiene todos los anuncios de un aula específica, ordenados por fecha de publicación descendente.
        """
        query = """
        SELECT id_anuncio, id_aula, titulo, descripcion, fecha_publicacion
        FROM anuncios
        WHERE id_aula = %s
        ORDER BY fecha_publicacion DESC
        """
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (id_aula,))
        result = cursor.fetchall()
        conn.close()
        return result

    def get_by_id(self, id_anuncio):
        """
        Obtiene un anuncio específico por su ID.
        """
        query = """
        SELECT id_anuncio, id_aula, titulo, descripcion, fecha_publicacion
        FROM anuncios
        WHERE id_anuncio = %s
        """
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (id_anuncio,))
        result = cursor.fetchone()
        conn.close()
        return result

    # ----------------------------------------
    # UPDATE
    # ----------------------------------------
    def update(self, id_anuncio, titulo, descripcion):
        """
        Actualiza el título o descripción de un anuncio.
        """
        query = """
        UPDATE anuncios
        SET titulo = %s, descripcion = %s
        WHERE id_anuncio = %s
        """
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(query, (titulo, descripcion, id_anuncio))
        conn.commit()
        conn.close()
        return True

    # ----------------------------------------
    # DELETE
    # ----------------------------------------
    def delete(self, id_anuncio):
        """
        Elimina un anuncio por su ID.
        """
        query = "DELETE FROM anuncios WHERE id_anuncio = %s"
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(query, (id_anuncio,))
        conn.commit()
        conn.close()
        return True
