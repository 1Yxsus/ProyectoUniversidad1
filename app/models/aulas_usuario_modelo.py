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

    def get_id_aula_usuario(self, id_aula, id_usuario):
        """
        Devuelve el id_aula_usuario (PK) para la combinación id_aula + id_usuario.
        Retorna int o None si no existe.
        """
        query = "SELECT id_aula_usuario FROM aulas_usuarios WHERE id_aula = %s AND id_usuario = %s LIMIT 1"
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (id_aula, id_usuario))
        row = cursor.fetchone()
        conn.close()
        if row and "id_aula_usuario" in row:
            try:
                return int(row["id_aula_usuario"])
            except Exception:
                return row["id_aula_usuario"]
        return None

    def get_rol_en_aula(self, id_aula, id_usuario):
        """
        Devuelve el rol (string) del usuario en la aula, o None si no existe.
        """
        query = "SELECT rol FROM aulas_usuarios WHERE id_aula = %s AND id_usuario = %s LIMIT 1"
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (int(id_aula), int(id_usuario)))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row.get("rol") if row else None

    def get_roles_por_usuario(self, id_usuario):
        """
        Devuelve dict { id_aula: rol } para todas las aulas donde está el usuario.
        """
        query = "SELECT id_aula, rol FROM aulas_usuarios WHERE id_usuario = %s"
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (int(id_usuario),))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return {r["id_aula"]: r["rol"] for r in rows} if rows else {}

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

    def asignar_admin(self, id_aula, nuevo_admin_id):
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            conn.start_transaction()
            # validar candidato en aula
            cursor.execute("SELECT COUNT(1) FROM aulas_usuarios WHERE id_aula = %s AND id_usuario = %s", (id_aula, nuevo_admin_id))
            if cursor.fetchone()[0] == 0:
                raise Exception("Usuario no pertenece a la aula")

            # demote any existing admins (opcional: permitir varios admins si quieres)
            cursor.execute("UPDATE aulas_usuarios SET rol = %s WHERE id_aula = %s AND rol = %s", ("ALUMNO", id_aula, "ADMIN"))

            # assign ADMIN to selected
            cursor.execute("UPDATE aulas_usuarios SET rol = %s WHERE id_aula = %s AND id_usuario = %s", ("ADMIN", id_aula, nuevo_admin_id))

            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()
        return True
