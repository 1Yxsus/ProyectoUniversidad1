from app.models.usuario_modelo import UsuarioModel

def authenticate_user(correo, password):
    usuario_model = UsuarioModel()
    users = usuario_model.get_by_credentials(correo, password)
    return users


def register_user(nombre: str, apellido: str, correo: str, contrasena: str):
    """
    Intenta registrar un usuario.
    Devuelve (True, None) si tuvo éxito.
    Devuelve (False, "mensaje") en caso de error o si el correo ya existe.
    """
    usuario_model = UsuarioModel()
    try:
        usuario_model.create(nombre, apellido, correo, contrasena)
        return True, None

    except Exception as ex:
        return False, str(ex)

def obtener_usuario_por_id(id_usuario: int):
    usuario_model = UsuarioModel()
    usuario = usuario_model.get_by_id(id_usuario)
    return usuario

def actualizar_usuario(id_usuario: int, nombres: str, apellidos: str, correo: str, contrasena: str):
    
    usuario_model = UsuarioModel()
    try:
        usuario_model.update(id_usuario, nombres, apellidos, correo, contrasena)
        return True, None
    except Exception as ex:
        return False, str(ex)