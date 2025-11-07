
from app.models.tareas_modelo import TareaModel

def crear_tarea(id_curso: int, titulo: str, descripcion: str, fecha_entrega: str, publicado_por: str):

    tarea_model = TareaModel()
    tarea_model.create(id_curso, titulo, descripcion, fecha_entrega, publicado_por)

def actualizar_tarea(id_tarea: int, titulo: str, descripcion: str, fecha_entrega: str, publicado_por: int):

    tarea_model = TareaModel()
    tarea_model.update(id_tarea, titulo, descripcion, fecha_entrega, publicado_por)

def obtener_tareas_por_curso(id_curso: int):

    tarea_model = TareaModel()
    return tarea_model.get_by_curso(id_curso)