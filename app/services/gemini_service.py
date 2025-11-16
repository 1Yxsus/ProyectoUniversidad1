import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class GeminiService:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            self.client = genai.Client(api_key=api_key)
            self._mode = "api_key"
        else:
            self.client = None
            self._mode = None
        self.prompt_template = """
        Extrae SOLO la información del punto IV. UNIDADES DE APRENDIZAJE.

        FORMATO EXACTO QUE DEBES DEVOLVER:

        Semana N° X
        [Tema 1 sin numeración, sin dos puntos]
        [Tema 2 sin numeración, sin dos puntos]
        [Tema 3 sin numeración, sin dos puntos]

        Semana N° Y
        [Tema 1 real]
        [Tema 2 real]
        ...

        REGLAS ESTRICTAS:
        - NO inventes temas, usa exactamente los que aparecen en el PDF.
        - NO reescribas ni resumas los temas, copia el texto literal.
        - NO pongas “Tema 1”, “Tema 2”, etc. SOLO el texto del tema.
        - NO agregues “:”.
        - NO enumeres los temas.
        - NO agregues comillas.
        - Cada tema debe ir en una nueva línea.
        - Cada semana debe estar separada por UNA línea en blanco.
        - Mantén el orden EXACTO en que aparecen en el syllabus.
        - Si una semana no tiene temas, déjala vacía debajo del título.

        Ejemplo de salida esperada:

        Semana N° 1
        [tema real 1]
        [tema real 2]
        [tema real 3]

        Semana N° 2
        [tema real 1]
        [tema real 2]
        [tema real 3]

        Ahora devuelve SOLO el resultado formateado, sin explicaciones.
        """


    def analizar_syllabus_pdf(self, file_bytes, file_name="syllabus.pdf"):
        if not self.client:
            return False, "GeminiService no configurado (faltó GEMINI_API_KEY)."

        try:
            pdf_part = types.Part.from_bytes(
                data=file_bytes,
                mime_type="application/pdf"
            )

            respuesta = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    self.prompt_template,
                    pdf_part,
                ],
            )

            # DEBUG opcional
            # print("RAW RESPONSE:", respuesta)
            # print("TEXT:", respuesta.text)

            return True, respuesta.text

        except Exception as e:
            # Aquí verás el mensaje real del error
            print("ERROR GEMINI:", repr(e))
            return False, str(e)

    def analizar_texto(self, texto):
        if not self.client:
            return False, "GeminiService no configurado (faltó GEMINI_API_KEY)."
        try:
            respuesta = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    "Analiza el siguiente texto y extrae semanas y temas:",
                    texto
                ]
            )
            return True, respuesta.text
        except Exception as e:
            print("ERROR GEMINI:", repr(e))
            return False, str(e)
