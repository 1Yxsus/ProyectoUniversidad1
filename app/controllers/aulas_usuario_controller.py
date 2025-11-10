from app.models.aulas_usuario_modelo import AulaUsuarioModel

def agregar_usuario_a_aula(id_aula: int, id_usuario: int, rol: str = "ALUMNO"):
    """
    Intenta agregar un usuario a un aula con un rol específico.
    Devuelve (True, None) si tuvo éxito.
    Devuelve (False, "mensaje") en caso de error.
    """
    aula_usuario_model = AulaUsuarioModel()
    try:
        aula_usuario_model.create(id_aula, id_usuario, rol)
        return True, None
    except Exception as ex:
        print("Error agregar_usuario_a_aula:", ex)
        return False, str(ex)

def asignar_admin_a_usuario(id_aula: int, nuevo_admin_id: int):
    model = AulaUsuarioModel()
    return model.asignar_admin(id_aula, nuevo_admin_id)

def obtener_miembros_de_aula(id_aula: int):
    """
    Devuelve la lista de miembros de un aula.
    Cada miembro es un diccionario con sus datos.
    """
    aula_usuario_model = AulaUsuarioModel()
    result = aula_usuario_model.get_by_aula(id_aula)
    return result

def obtener_rol_usuario_en_aula(id_aula, id_usuario):
    model = AulaUsuarioModel()
    return model.get_rol_en_aula(id_aula, id_usuario)

def obtener_roles_por_usuario(id_usuario):
    model = AulaUsuarioModel()
    return model.get_roles_por_usuario(id_usuario)

def eliminar_usuario_de_aula(id_aula: int,id_usuario: int):
    """
    Intenta eliminar un usuario de un aula.
    Devuelve (True, None) si tuvo éxito.
    Devuelve (False, "mensaje") en caso de error.
    """
    aula_usuario_model =AulaUsuarioModel()
    try:
        id_usuario_aula = aula_usuario_model.get_id_aula_usuario(id_aula, id_usuario)
        if not id_usuario_aula:
            raise Exception("El usuario no pertenece al aula")
        aula_usuario_model.delete(id_usuario_aula)
        return True, None
    except Exception as ex:
        print("Error eliminar_usuario_de_aula:", ex)
        return False, str(ex)