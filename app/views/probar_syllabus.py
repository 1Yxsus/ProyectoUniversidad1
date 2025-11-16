import flet as ft
from app.controllers.syllabus_controller import procesar_syllabus_pdf
import os, traceback

def TestGeminiView(page: ft.Page):

    page.title = "Prueba de Gemini IA"
    page.bgcolor = ft.Colors.BLACK
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.snack_bar = ft.SnackBar(content=ft.Text(""), bgcolor=ft.Colors.GREY_900)

    resultado_text = ft.Text(
        value="Aquí aparecerá el resultado...",
        color=ft.Colors.WHITE,
        size=14,
        selectable=True,
    )

    def subir_archivo(e: ft.FilePickerResultEvent):
        if not e.files:
            return

        archivo = e.files[0]

        with open(archivo.path, "rb") as f:
            file_bytes = f.read()

        page.snack_bar.content = ft.Text("Procesando PDF con Gemini...")
        page.snack_bar.open = True
        page.update()

        # DEBUG: verificar longitud de bytes y variable de entorno de Gemini
        print("DEBUG: archivo.path =", archivo.path)
        print("DEBUG: file_bytes len =", len(file_bytes))
        print("DEBUG: GEMINI_API_KEY =", bool(os.getenv("GEMINI_API_KEY")))

        try:
            # llamar al controlador y capturar excepciones
            success, response = procesar_syllabus_pdf(file_bytes)
        except Exception as ex:
            traceback.print_exc()
            page.snack_bar.content = ft.Text("Excepción al procesar. Revisa la consola.")
            page.snack_bar.open = True
            page.update()
            return

        # mostrar resultado de debug si falla
        print("DEBUG: procesar_syllabus_pdf returned:", success, type(response))


        # Aquí manda el archivo al controlador
        if not success:
            # response puede ser mensaje de error o excepción como string
            page.snack_bar.content = ft.Text("ERROR: " + str(response))
            page.snack_bar.open = True
            page.update()
            return

        # success -> actualizar UI con la respuesta (puede ser texto)
        resultado_text.value = str(response)
        page.update()

        page.snack_bar.content = ft.Text("Procesado exitoso.")
        page.snack_bar.open = True
        page.update()

    picker = ft.FilePicker(on_result=subir_archivo)
    page.overlay.append(picker)

    btn_subir = ft.ElevatedButton(
        "Subir PDF para probar Gemini",
        icon=ft.Icons.UPLOAD_FILE,
        on_click=lambda e: picker.pick_files(allow_multiple=False),
        bgcolor=ft.Colors.BLUE_700,
        color=ft.Colors.WHITE,
    )

    return ft.Column(
        [
            ft.Container(height=30),
            btn_subir,
            ft.Container(height=30),
            resultado_text,
        ],
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
