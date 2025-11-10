from app.models.syllabus_modelo import SyllabusModel

def get_syllabus_by_curso(id_curso: int):
    """
    Devuelve el registro del syllabus (dict) o None.
    """
    modelo = SyllabusModel()

    try:
        return modelo.get_by_curso(int(id_curso))
    except Exception:
        return None

def get_texto_syllabus_por_curso(id_curso: int) -> str:
    """
    Devuelve solo el texto del syllabus o cadena vacía si no existe.
    """
    rec = get_syllabus_by_curso(id_curso)
    return (rec.get("texto_syllabus") if rec and isinstance(rec, dict) else "") or ""


def create_syllabus(id_curso, texto_syllabus):
    """
    Controlador para crear un nuevo syllabus.
    """

    modelo = SyllabusModel()
    return modelo.create(id_curso, texto_syllabus)

def update_syllabus(id_syllabus, texto):

    modelo = SyllabusModel()
    return modelo.update(id_syllabus, texto)

def update_syllabus_by_curso(id_curso, texto):
    modelo = SyllabusModel()
    return modelo.update_by_curso(int(id_curso), texto)

def get_syllabus_by_curso(id_curso):
    """
    Controlador para obtener el syllabus de un curso específico.
    """
    modelo = SyllabusModel()
    return modelo.get_by_curso(id_curso)