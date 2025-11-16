import flet as ft
from app.utils.vald_text_fields import validar_formulario
from app.controllers.syllabus_controller import (
    create_syllabus, get_syllabus_by_curso,
    get_texto_syllabus_por_curso, update_syllabus_by_curso, procesar_syllabus_pdf
)
from app.utils.is_staff_verification import is_staff_verification
from app.utils.show_succes import show_success
import os, traceback

def SyllabusCursoView(page: ft.Page, curso_dict: dict, id_aula, func_load_content):
    """
    Vista estilizada dark-petróleo para visualizar y editar el syllabus.
    Incluye modal de instrucciones con IA y tarjetas de semanas.
    """

    # ==============================================================
    # COLORES BASE
    # ==============================================================
    COLOR_BG_CARD = "#0E1E25"
    COLOR_BG_CARD_HOVER = "#152B33"
    COLOR_BORDER_CARD = "#1F3A44"
    COLOR_ACCENT = "#1C8DB0"
    COLOR_TEXT_PRIMARY = "#EAEAEA"
    COLOR_TEXT_SECONDARY = "#AAB6B8"

    # ==============================================================
    # LÓGICA PRINCIPAL
    # ==============================================================
    is_staff = is_staff_verification(page, curso_dict["id_aula"])

    def procesar_syllabus(texto: str):
        bloques, bloque_actual = [], []
        for linea in texto.splitlines():
            if not linea.strip():
                if bloque_actual:
                    bloques.append("\n".join(bloque_actual))
                    bloque_actual = []
            else:
                bloque_actual.append(linea.strip())
        if bloque_actual:
            bloques.append("\n".join(bloque_actual))

        resultado = []
        for bloque in bloques:
            lineas = [l.strip() for l in bloque.split("\n") if l.strip()]
            if not lineas:
                continue
            resultado.append({
                "semana": lineas[0],
                "temas": lineas[1:]
            })
        return resultado

    # ==============================================================
    # VARIABLES Y ENCABEZADO
    # ==============================================================
    curso_nombre = curso_dict.get("curso")
    curso_id = curso_dict.get("id_curso")

    titulo_curso = ft.Text(curso_nombre, size=36, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_PRIMARY)

    btn_editar = ft.IconButton(
        icon=ft.Icons.EDIT,
        icon_color=COLOR_ACCENT,
        tooltip="Editar syllabus",
        style=ft.ButtonStyle(shape=ft.CircleBorder(), bgcolor="#122A33"),
    )

    btn_agregar = ft.Container(
        content=ft.Row(
            [ft.Icon(ft.Icons.ADD, color="#FFFFFF"), ft.Text("Agregar Syllabus", color="#FFFFFF")],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=6,
        ),
        gradient=ft.LinearGradient(colors=[COLOR_ACCENT, "#145C70"]),
        width=190,
        height=45,
        border_radius=8,
        ink=True,
        on_click=lambda e: abrir_modal(e),
    )

    btn_volver = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_color="#EAEAEA",
        style=ft.ButtonStyle(shape=ft.CircleBorder(), bgcolor="#122A33"),
        tooltip="Volver",
        on_click=lambda e: func_load_content("Curso", curso_dict),
    )

    btn_home = ft.IconButton(
        icon=ft.Icons.HOME,
        icon_color="#EAEAEA",
        style=ft.ButtonStyle(shape=ft.CircleBorder(), bgcolor="#122A33"),
        tooltip="Inicio",
        on_click=lambda e: page.go("/options"),
    )

    header = ft.Row(
        [titulo_curso, ft.Container(expand=True), ft.Row([btn_editar, btn_agregar, btn_volver, btn_home])],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    subtitulo = ft.Text("Syllabus", size=22, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_SECONDARY)

    # ==============================================================
    # TEXTAREA PRINCIPAL
    # ==============================================================
    text_area_syllabus = ft.TextField(
        label="Texto del Syllabus:",
        bgcolor="#0D1A20",
        border_radius=8,
        border_color="#1F3A44",
        focused_border_color=COLOR_ACCENT,
        color=COLOR_TEXT_PRIMARY,
        multiline=True,
        min_lines=6,
        max_lines=10,
    )

    texto_inicial = get_texto_syllabus_por_curso(curso_id) or ""
    text_area_syllabus.value = texto_inicial

    btn_agregar.visible = bool(is_staff) and not bool(texto_inicial)
    btn_editar.visible = bool(is_staff) and bool(texto_inicial)

    # ==============================================================
    # MODALES: CREAR / EDITAR Y MODAL DE INSTRUCCIONES
    # ==============================================================
    edit_mode = False

    def abrir_modal(e=None):
        nonlocal edit_mode
        edit_mode = False
        modal_title.value = "AÑADIR SYLLABUS"
        btn_guardar.text = "CREAR"
        modal_container.visible = True
        page.update()

    def abrir_modal_editar(e=None):
        nonlocal edit_mode
        edit_mode = True
        modal_title.value = "EDITAR SYLLABUS"
        btn_guardar.text = "GUARDAR"
        modal_container.visible = True
        page.update()

    btn_editar.on_click = abrir_modal_editar

    def cerrar_modal(e=None):
        modal_container.visible = False
        page.update()

    # --------------------------------------------------------------
    # FUNCIONES DE GUARDADO
    # --------------------------------------------------------------
    def validar_y_guardar(e):
        if not validar_formulario(page, [text_area_syllabus]):
            return
        try:
            existing = get_syllabus_by_curso(curso_id)
            if existing:
                update_syllabus_by_curso(curso_id, text_area_syllabus.value)
            else:
                create_syllabus(curso_id, text_area_syllabus.value)
            reload_syllabus()
            cerrar_modal()
            show_success(page, "✅ Syllabus guardado correctamente")
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al guardar: {ex}"), bgcolor="#A93226")
            page.snack_bar.open = True
        page.update()

    # --------------------------------------------------------------
    # MODAL PRINCIPAL
    # --------------------------------------------------------------
    # --- Estado interno ---
    selected_option = ft.Ref[ft.Dropdown]()
    upload_button = ft.Ref[ft.ElevatedButton]()

    # --- Control dinámico según selección ---
    def on_option_change(e):
        opcion = selected_option.current.value if selected_option and selected_option.current else None

        # mostrar/ocultar botón subir archivo (si el ref ya está disponible)
        mostrar_upload = opcion in ("Subir PDF", "Subir Word")
        if upload_button and upload_button.current:
            upload_button.current.visible = mostrar_upload

        # text_area_syllabus es un control directo (no Ref) — actualizar su visible directamente
        if opcion in ("Subir PDF", "Subir Word", "Subir Texto"):
            text_area_syllabus.visible = True
        else:
            text_area_syllabus.visible = False

        page.update()

    # --- FilePicker handler para procesar PDFs/DOCs con IA ---
    def on_file_picked(e: ft.FilePickerResultEvent):
        if not e.files:
            return
        archivo = e.files[0]
        try:
            with open(archivo.path, "rb") as f:
                file_bytes = f.read()
        except Exception as ex:
            traceback.print_exc()
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Error al leer archivo: {ex}"), bgcolor="#A93226")
            page.snack_bar.open = True
            page.update()
            return

        # mostrar overlay de carga
        # traer loading_overlay al frente y mostrarlo
        if loading_overlay in page.overlay:
            try:
                page.overlay.remove(loading_overlay)
            except Exception:
                pass
        page.overlay.append(loading_overlay)
        loading_overlay.visible = True
        page.update()


        page.snack_bar = ft.SnackBar(content=ft.Text("Procesando archivo con IA..."))
        page.snack_bar.open = True
        page.update()

        try:
            success, response = procesar_syllabus_pdf(file_bytes)
            print("DEBUG: procesar_syllabus - file len =", len(file_bytes), "curso_id=", curso_id)
        except Exception as ex:
            traceback.print_exc()
            # ocultar overlay de carga al fallar
            loading_overlay.visible = False
            page.update()
            page.snack_bar = ft.SnackBar(content=ft.Text("Excepción al procesar: revisa consola"), bgcolor="#A93226")
            page.snack_bar.open = True
            page.update()
            return

        if not success:
            # ocultar overlay de carga si la IA devolvió error
            loading_overlay.visible = False
            page.update()
            page.snack_bar = ft.SnackBar(content=ft.Text(f"ERROR: {response}"), bgcolor="#A93226")
            page.snack_bar.open = True
            page.update()
            return

        # response esperado: texto del syllabus procesado por la IA
        print("DEBUG: procesar_syllabus response type=", type(response))
        text_area_syllabus.value = str(response)

        # ocultar overlay de carga al completar correctamente
        loading_overlay.visible = False
        page.update()


        page.snack_bar = ft.SnackBar(content=ft.Text("Syllabus generado y guardado ✅"))
        page.snack_bar.open = True
        page.update()

    file_picker = ft.FilePicker(on_result=on_file_picked)
    
    # --- Overlay de carga (progress) --- (añadir UNA vez)
    # fondo muy tenue para que NO 'desaparezca' el contenido de fondo
    loading_overlay = ft.Container(
        bgcolor=ft.Colors.with_opacity(0.12, "#000000"),  # menos opaco
        expand=True,
        alignment=ft.alignment.center,
        visible=False,
        # caja central también semi-transparente para ver fondo a través de ella
        content=ft.Container(
            padding=16,
            border_radius=12,
            bgcolor=ft.Colors.with_opacity(0.80, "#0B1418"),
            content=ft.Column(
                [
                    ft.ProgressRing(width=60, height=60),
                    ft.Container(height=12),
                    ft.Text("""Procesando con IA...
                            Recuerda que los resultados pueden llegar a ser los no acertados, asegurate de revisarlo.""", color=COLOR_TEXT_PRIMARY, text_align=ft.TextAlign.CENTER),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
       ),
    )
    # añadir overlay de carga (solo una vez)
    if loading_overlay not in page.overlay:
        page.overlay.append(loading_overlay)

    # --- Dropdown de selección ---
    dropdown_opciones = ft.Dropdown(
        ref=selected_option,
        label="Selecciona cómo deseas ingresar el syllabus",
        options=[
            ft.dropdown.Option("Subir PDF"),
            ft.dropdown.Option("Subir Word"),
            ft.dropdown.Option("Subir Texto"),
        ],
        width=300,
        on_change=on_option_change,
    )

    # --- Botón subir archivo ---
    btn_subir_archivo = ft.ElevatedButton(
        ref=upload_button,
        text="Subir archivo",
        icon=ft.Icons.UPLOAD_FILE,
        visible=False,
        bgcolor="#123944",
        color="#FFFFFF",
        on_click=lambda e: file_picker.pick_files(allow_multiple=False)
    )

    # --- TextField si se elige “Subir texto” ---

    # --- Título y botones del modal ---
    modal_title = ft.Text(
        "AÑADIR SYLLABUS",
        weight=ft.FontWeight.BOLD,
        size=22,
        color=COLOR_TEXT_PRIMARY
    )

    btn_guardar = ft.Container(
        content=ft.Text("Guardar", color="#FFFFFF", size=16),
        gradient=ft.LinearGradient(colors=[COLOR_ACCENT, "#145C70"]),
        width=150,
        height=45,
        border_radius=8,
        alignment=ft.alignment.center,
        ink=True,
        on_click=validar_y_guardar,
    )

    btn_cancelar = ft.Container(
        content=ft.Text("Cancelar", color=COLOR_TEXT_SECONDARY, size=16),
        border=ft.border.all(1, "#2C2C2C"),
        border_radius=8,
        width=120,
        height=45,
        alignment=ft.alignment.center,
        ink=True,
        on_click=cerrar_modal,
    )

    # --- NUEVO CONTENIDO DEL MODAL (sin instrucciones) ---
    modal_container = ft.Container(
        bgcolor=ft.Colors.with_opacity(0.65, "#000000"),
        expand=True,
        alignment=ft.alignment.center,
        visible=False,
        content=ft.Container(
            width=700,
            height=600,
            bgcolor="#0B1418",
            border_radius=12,
            border=ft.border.all(1, "#1E2C30"),
            padding=30,
            content=ft.Column(
                [
                    ft.Row(
                        [ft.Icon(ft.Icons.BOOK_OUTLINED, color=COLOR_ACCENT), modal_title],
                        spacing=10
                    ),

                    # --- Nuevo dropdown para seleccionar el método ---
                    ft.Text(
                        "Método de ingreso de syllabus",
                        size=16,
                        color=COLOR_TEXT_SECONDARY,
                        weight=ft.FontWeight.BOLD
                    ),

                    dropdown_opciones,
                    btn_subir_archivo,

                    # --- Campo original del syllabus (texto final procesado) ---
                    text_area_syllabus,

                    ft.Row(
                        [btn_cancelar, btn_guardar],
                        alignment=ft.MainAxisAlignment.END,
                        spacing=12
                    ),
                ],
                spacing=15,
            ),
        ),
    )

    # Añadir modal al overlay
    # asegurarse de añadir el modal y el file_picker al overlay (modal antes que loading)
    if modal_container not in page.overlay:
        page.overlay.append(modal_container)
    if file_picker not in page.overlay:
        page.overlay.append(file_picker)
    # asegurar que el loading_overlay esté al final (por si se añadió antes): reinsertarlo para traerlo al frente
    if loading_overlay in page.overlay:
        try:
            page.overlay.remove(loading_overlay)
        except Exception:
            pass
    page.overlay.append(loading_overlay)

    # ==============================================================
    # TARJETAS DE SEMANAS
    # ==============================================================
    def card_semana(semana, temas):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(semana, size=18, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_PRIMARY),
                    ft.Column(
                        [ft.Text(f"• {t}", color=COLOR_TEXT_SECONDARY, size=14) for t in temas],
                        spacing=6,
                        scroll=ft.ScrollMode.AUTO,
                    ),
                ],
                spacing=8,
            ),
            bgcolor=ft.LinearGradient(colors=[COLOR_BG_CARD, "#0C252D"]),
            border=ft.border.all(1, COLOR_BORDER_CARD),
            border_radius=12,
            width=220,
            height=220,
            padding=ft.padding.all(12),
            ink=True,
            on_hover=lambda e: (
                setattr(
                    e.control,
                    "bgcolor",
                    ft.LinearGradient(colors=[COLOR_BG_CARD_HOVER, "#133540"])
                    if e.data == "true"
                    else ft.LinearGradient(colors=[COLOR_BG_CARD, "#0C252D"]),
                ),
                e.control.update(),
            ),
        )

    def grid_semanas(lista):
        return ft.Container(
            content=ft.Column(
                [
                    ft.ResponsiveRow(
                        [ft.Container(card_semana(s["semana"], s["temas"]), col={"sm": 6, "md": 4, "lg": 3}) for s in lista],
                        spacing=20,
                        run_spacing=20,
                    )
                ],
                scroll=ft.ScrollMode.AUTO,
            ),
            expand=True,
            alignment=ft.alignment.top_center,
        )

    # ==============================================================
    # RELOAD Y CONTENIDO PRINCIPAL
    # ==============================================================
    syllabus_data = procesar_syllabus(texto_inicial)
    lista_semanas = grid_semanas(syllabus_data)

    def reload_syllabus():
        nonlocal lista_semanas
        texto_nuevo = get_texto_syllabus_por_curso(curso_id) or ""
        data = procesar_syllabus(texto_nuevo)
        lista_semanas.content.controls = [
            ft.ResponsiveRow(
                [ft.Container(card_semana(s["semana"], s["temas"]), col={"sm": 6, "md": 4, "lg": 3}) for s in data],
                spacing=20,
                run_spacing=20,
            )
        ]
        text_area_syllabus.value = texto_nuevo
        page.update()

    contenido = ft.Column(
        [header, ft.Container(height=30), subtitulo, lista_semanas],
        spacing=20,
        expand=True,
    )

    layout = ft.Container(
        content=contenido,
        expand=True,
        padding=ft.padding.all(50),
    )

    # modal_container ya está en page.overlay, no lo incluimos aquí para evitar duplicados/z-index issues
    return ft.Stack(
        [
           ft.Container(
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=["#0C1C24", "#0E2329", "#08171C"],
                ),
                expand=True,
            ),
            layout,
        ],
        expand=True,
    )
