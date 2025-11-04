from app.models.cursos_modelo import CursoModel
from app.models.usuario_modelo import UsuarioModel

def obtener_cursos(id_aula: int):
    """
    Devuelve la lista de todos los cursos a los que el usuario tiene acceso.
    """

    curso_model = CursoModel()
    result = curso_model.get_by_aula(id_aula)

    cursos = [ { "id_aula": id_aula, "id_curso" : c["id_curso"] , "curso" : c["nombre_curso"], "docente" : c["nombre_docente"], "delegado" : c["nombre_delegado"], "id_delegado" : c["id_delegado"]} for c in result ]


    return cursos

def crear_curso(id_aula: int, nombre_curso: str, descripcion: str, id_delegado: int = None):
    """
    Crea un nuevo curso en el aula especificada.
    """

    usuario_modelo = UsuarioModel()

    delegado = None

    if id_delegado is not None:
        delegado = usuario_modelo.get_by_id(id_delegado)
        if delegado is None:
            raise ValueError(f"El delegado con ID {id_delegado} no existe.")

    curso_model = CursoModel()

    delegado = delegado["nombre"] + " " + delegado["apellido"] if delegado else None

    curso_model.create(id_aula, nombre_curso, descripcion, id_delegado, delegado)

def actualizar_curso(id_curso: int, nombre_curso: str, name_docente: str, id_delegado: int = None):
    """
    Actualiza los datos de un curso existente.
    """

    usuario_modelo = UsuarioModel()

    delegado = None

    if id_delegado is not None:
        delegado = usuario_modelo.get_by_id(id_delegado)
        if delegado is None:
            raise ValueError(f"El delegado con ID {id_delegado} no existe.")

    curso_model = CursoModel()

    delegado = delegado["nombre"] + " " + delegado["apellido"] if delegado else None

    curso_model.update(id_curso, nombre_curso, name_docente, id_delegado, delegado)