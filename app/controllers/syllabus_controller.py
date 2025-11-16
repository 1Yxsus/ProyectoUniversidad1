from app.models.syllabus_modelo import SyllabusModel
from app.services.gemini_service import GeminiService
from google import genai
import os

try:
    c = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    r = c.models.generate_content(model="gemini-2.0-flash", contents=["Hola"])
    print("OK:", type(r), getattr(r, "text", str(r)))
except Exception as e:
    print("ERROR:", e)

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

gemini = GeminiService()

def procesar_syllabus_pdf(file_bytes):
    """
    Envía un PDF a Gemini, guarda el resultado en BD y lo retorna.
    """
    success, resultado = gemini.analizar_syllabus_pdf(file_bytes)

    if not success:
        return False, f"Error procesando PDF con IA: {resultado}"
    
    return True, resultado