from app.models.aulas_modelo import AulaModel
from app.models.aulas_usuario_modelo import AulaUsuarioModel

def crear_aulas(nombre_aula: str, descripcion: str, id_admin: int):
    """
    Intenta crear un aula.
    Devuelve (True, None) si tuvo éxito.
    Devuelve (False, "mensaje") en caso de error.
    """
    aula_model = AulaModel()
    aula_usuario_model = AulaUsuarioModel()
    try:
        inserted_id = aula_model.create(nombre_aula, descripcion, id_admin)
        if not inserted_id:
            raise Exception("No se obtuvo id del aula creada")
        aula_usuario_model.create(inserted_id, id_admin, rol="ADMIN")
        return True, None
    except Exception as ex:

        print("Error crear_aulas:", ex)
        return False, str(ex)
    
def obtener_aulas(id_usuario: int):
    """
    Devuelve la lista de todas las aulas.
    """
    aula_model = AulaModel()
    result = aula_model.get_by_usuario(id_usuario)

    return result

def obtener_aula_by_id(id_aula: int):
    """
    Devuelve un diccionario con los datos del aula.
    """
    aula_model = AulaModel()
    result = aula_model.get_by_id(id_aula)
    if result:
        return result
    else:
        return None

def actualizar_aula(id_aula: int, nombre_aula: str, descripcion: str):
    """
    Intenta actualizar un aula.
    Devuelve (True, None) si tuvo éxito.
    Devuelve (False, "mensaje") en caso de error.
    """
    aula_model =AulaModel()
    try:
        updated_rows = aula_model.update(id_aula, nombre_aula, descripcion)
        if updated_rows == 0:
            raise Exception("No se actualizó ningún registro")
        return True, None
    except Exception as ex:
        print("Error actualizar_aula:", ex)
        return False, str(ex)