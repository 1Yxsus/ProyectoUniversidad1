# from app.utils.database import DatabaseConnection

# class CursoModel:
#     def __init__(self):
#         self.db = DatabaseConnection()

#     def create(self, id_aula, nombre_curso, nombre_docente, id_delegado=None, nombre_delegado=None):
#         query = "INSERT INTO cursos (id_aula, nombre_curso, nombre_docente, id_delegado, nombre_delegado) VALUES (%s, %s, %s, %s, %s)"
#         conn = self.db.connect()
#         cursor = conn.cursor()
#         cursor.execute(query, (id_aula, nombre_curso, nombre_docente, id_delegado, nombre_delegado))
#         conn.commit()
#         conn.close()

#     def get_by_aula(self, id_aula):
#         query = "SELECT * FROM cursos WHERE id_aula = %s"
#         conn = self.db.connect()
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute(query, (id_aula,))
#         result = cursor.fetchall()
#         conn.close()
#         return result
    
#     def get_by_usuario(self, id_usuario):
#         """
#         Obtiene todos los cursos a los que el usuario tiene acceso,
#         según las aulas a las que pertenece.
#         """
#         query = """
#         SELECT 
#             c.id_curso,
#             c.nombre_curso,
#             c.descripcion,
#             c.id_aula,
#             a.nombre_aula,
#             au.rol
#         FROM cursos c
#         JOIN aulas a ON c.id_aula = a.id_aula
#         JOIN aulas_usuarios au ON a.id_aula = au.id_aula
#         WHERE au.id_usuario = %s
#         ORDER BY a.nombre_aula, c.nombre_curso
#         """
#         conn = self.db.connect()
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute(query, (id_usuario,))
#         result = cursor.fetchall()
#         conn.close()
#         return result
    
#     def get_by_aula(self, id_aula):
#         """
#         Obtiene todos los cursos que pertenecen a un aula específica.
#         """
#         query = """
#         SELECT 
#             c.id_curso,
#             c.nombre_curso,
#             c.descripcion,
#             c.id_aula,
#             a.nombre_aula,
#             u.nombre AS delegado_nombre,
#             u.apellido AS delegado_apellido
#         FROM cursos c
#         JOIN aulas a ON c.id_aula = a.id_aula
#         LEFT JOIN usuarios u ON c.id_delegado = u.id_usuario
#         WHERE c.id_aula = %s
#         ORDER BY c.fecha_creacion DESC
#         """
#         conn = self.db.connect()
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute(query, (id_aula,))
#         result = cursor.fetchall()
#         conn.close()
#         return result

#     def update(self, id_curso, nombre_curso, descripcion):
#         query = "UPDATE cursos SET nombre_curso=%s, descripcion=%s WHERE id_curso=%s"
#         conn = self.db.connect()
#         cursor = conn.cursor()
#         cursor.execute(query, (nombre_curso, descripcion, id_curso))
#         conn.commit()
#         conn.close()

#     def delete(self, id_curso):
#         query = "DELETE FROM cursos WHERE id_curso=%s"
#         conn = self.db.connect()
#         cursor = conn.cursor()
#         cursor.execute(query, (id_curso,))
#         conn.commit()
#         conn.close()

from app.utils.database import DatabaseConnection
import mysql.connector # Importar para manejar excepciones

class CursoModel:
    def __init__(self):
        self.db = DatabaseConnection()

    def create(self, id_aula, nombre_curso, nombre_docente, id_delegado, nombre_delegado):
        """
        Crea un nuevo curso en la base de datos.
        """
        query = "INSERT INTO cursos (id_aula, nombre_curso, nombre_docente, id_delegado, nombre_delegado) VALUES (%s, %s, %s, %s, %s)"
        conn = self.db.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (id_aula, nombre_curso, nombre_docente, id_delegado, nombre_delegado))
            conn.commit()
            return cursor.lastrowid # Devuelve el ID del curso creado
        except mysql.connector.Error as err:
            print(f"Error al crear curso: {err}")
            conn.rollback()
            return None
        finally:
            conn.close()

    def get_by_usuario(self, id_usuario):
        """
        Obtiene todos los cursos a los que el usuario tiene acceso,
        según las aulas a las que pertenece.
        """
        query = """
        SELECT 
            c.id_curso,
            c.nombre_curso,
            c.nombre_docente,
            c.id_delegado,
            c.nombre_delegado,
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
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (id_usuario,))
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error al obtener cursos por usuario: {err}")
            return []
        finally:
            conn.close()
    
    def get_by_aula(self, id_aula):
        """
        Obtiene todos los cursos que pertenecen a un aula específica.
        """
        query = """
        SELECT 
            c.id_curso,
            c.nombre_curso,
            c.nombre_docente,
            c.id_delegado,
            c.nombre_delegado,
            c.id_aula,
            a.nombre_aula,
            u.nombre AS delegado_nombre_user,
            u.apellido AS delegado_apellido_user
        FROM cursos c
        JOIN aulas a ON c.id_aula = a.id_aula
        LEFT JOIN usuarios u ON c.id_delegado = u.id_usuario
        WHERE c.id_aula = %s
        ORDER BY c.fecha_creacion DESC
        """
        conn = self.db.connect()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (id_aula,))
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error al obtener cursos por aula: {err}")
            return []
        finally:
            conn.close()

    def get_by_id(self, id_curso):
        """
        Obtiene un curso específico por su ID.
        """
        query = "SELECT * FROM cursos WHERE id_curso = %s"
        conn = self.db.connect()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (id_curso,))
            result = cursor.fetchone()
            return result
        except mysql.connector.Error as err:
            print(f"Error al obtener curso por ID: {err}")
            return None
        finally:
            conn.close()

    def get_nombre_by_id(self, id_curso):
        """
        Obtiene el nombre de un curso específico por su ID.
        """
        query = "SELECT nombre_curso FROM cursos WHERE id_curso = %s"
        conn = self.db.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (id_curso,))
            result = cursor.fetchone()
            return result[0] if result else None
        except mysql.connector.Error as err:
            print(f"Error al obtener nombre del curso por ID: {err}")
            return None
        finally:
            conn.close()

    def update(self, id_curso, nombre_curso, nombre_docente, id_delegado, nombre_delegado):
        """
        Actualiza los datos de un curso específico.
        """
        query = """
            UPDATE cursos 
            SET nombre_curso=%s, nombre_docente=%s, id_delegado=%s, nombre_delegado=%s 
            WHERE id_curso=%s
        """
        conn = self.db.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (nombre_curso, nombre_docente, id_delegado, nombre_delegado, id_curso))
            conn.commit()
            return cursor.rowcount # Devuelve 1 si la actualización fue exitosa, 0 si no
        except mysql.connector.Error as err:
            print(f"Error al actualizar curso: {err}")
            conn.rollback()
            return 0
        finally:
            conn.close()

    def delete(self, id_curso):
        """
        Elimina un curso de la base de datos.
        """
        query = "DELETE FROM cursos WHERE id_curso=%s"
        conn = self.db.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(query, (id_curso,))
            conn.commit()
            return cursor.rowcount # Devuelve 1 si se eliminó, 0 si no
        except mysql.connector.Error as err:
            print(f"Error al eliminar curso: {err}")
            conn.rollback()
            return 0
        finally:
            conn.close()

    