from app.models.anuncios_modelo import AnunciosModel

modelo = AnunciosModel()

def crear_anuncio(id_aula, titulo, descripcion):
    """
    Controlador para crear un nuevo anuncio.
    """
    return modelo.create(id_aula, titulo, descripcion)

def obtener_anuncios_por_aula(id_aula):
    """
    Controlador para obtener todos los anuncios de un aula específica.
    """
    return modelo.get_by_aula(id_aula)

def actualizar_anuncio(id_anuncio, titulo, descripcion):
    """
    Controlador para actualizar un anuncio existente.
    """
    return modelo.update(id_anuncio, titulo, descripcion)