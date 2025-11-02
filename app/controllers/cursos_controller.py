from app.models.cursos_modelo import CursoModel

def obtener_cursos(id_aula: int):
    """
    Devuelve la lista de todos los cursos a los que el usuario tiene acceso.
    """

    curso_model = CursoModel()
    result = curso_model.get_by_aula(id_aula)

    return result