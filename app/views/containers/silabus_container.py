import flet as ft
from app.utils.vald_text_fields import validar_formulario
from app.controllers.syllabus_controller import (
    create_syllabus, get_syllabus_by_curso,
    get_texto_syllabus_por_curso, update_syllabus_by_curso
)
from app.utils.is_staff_verification import is_staff_verification


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
    # INSTRUCCIONES (IA)
    # --------------------------------------------------------------
    prompt_texto = """
    Quiero que identifiques el punto IV. UNIDADES DE APRENDIZAJE, seleccionando la columna SEMANA y CONTENIDO TEMÁTICO del syllabus.
    Dame el resultado en formato bash, así:
    Semana N° 1 Tema 1: ... Tema 2: ... Tema 3: ...
    Semana N° 2 Tema 1: ... Tema 2: ... Tema 3: ...
    Y así sucesivamente hasta la última semana del documento, dejando un salto en línea por cada semana con su respectivo tema.
    """

    instruccion_texto = f"""Los docentes suelen enviar el syllabus en formato PDF o Word.
Para adaptarlo a la plataforma, utiliza una herramienta de inteligencia artificial (ChatGPT, Gemini, u otra).
Sube el archivo del syllabus y pega el siguiente prompt (usa el botón de copiar).
El resultado en formato especial se debe pegar en el campo de texto del syllabus.
    """

    def abrir_modal_instruccion(e=None):
        modal_instruccion.visible = True
        page.update()

    def cerrar_modal_instruccion(e=None):
        modal_instruccion.visible = False
        page.update()

    def copiar_instruccion(e=None):
        page.set_clipboard(prompt_texto)
        page.snack_bar = ft.SnackBar(ft.Text("📋 Instrucción copiada al portapapeles"))
        page.snack_bar.open = True
        page.update()

    btn_copiar_instruccion_inline = ft.IconButton(
        icon=ft.Icons.CONTENT_COPY,
        tooltip="Copiar instrucción",
        on_click=copiar_instruccion,
        icon_color=COLOR_ACCENT,
        bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.WHITE),
    )

    modal_instruccion = ft.Container(
        bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.BLACK),
        expand=True,
        alignment=ft.alignment.center,
        visible=False,
        content=ft.Container(
            width=520,
            height=260,
            bgcolor="#0B1418",
            border_radius=12,
            border=ft.border.all(1, "#1E2C30"),
            padding=20,
            content=ft.Column(
                [
                    ft.Row([
                        ft.Text("Instrucción IA", size=18, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_PRIMARY),
                        ft.Container(expand=True),
                        btn_copiar_instruccion_inline,
                        ft.IconButton(icon=ft.Icons.CLOSE, on_click=cerrar_modal_instruccion, icon_color="#AAAAAA")
                    ]),
                    ft.Divider(height=10, color="#1E2C30"),
                    ft.Text(instruccion_texto, color=COLOR_TEXT_SECONDARY, selectable=True, size=14),
                    ft.Row(
                        [
                            ft.Container(expand=True),
                            ft.Container(
                                content=ft.Text("Copiar instrucción", color="#FFFFFF"),
                                gradient=ft.LinearGradient(colors=[COLOR_ACCENT, "#145C70"]),
                                border_radius=8,
                                width=170,
                                height=40,
                                alignment=ft.alignment.center,
                                ink=True,
                                on_click=copiar_instruccion,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.END
                    ),
                ],
                spacing=10,
            ),
        ),
    )

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
            page.snack_bar = ft.SnackBar(ft.Text("✅ Syllabus guardado correctamente"))
            page.snack_bar.open = True
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al guardar: {ex}"), bgcolor="#A93226")
            page.snack_bar.open = True
        page.update()

    # --------------------------------------------------------------
    # MODAL PRINCIPAL
    # --------------------------------------------------------------
    modal_title = ft.Text("AÑADIR SYLLABUS", weight=ft.FontWeight.BOLD, size=22, color=COLOR_TEXT_PRIMARY)
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
    btn_instruccion = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.REMOVE_RED_EYE, color="#FFFFFF"),
                ft.Text("Ver instrucción", color="#FFFFFF", size=15, weight=ft.FontWeight.BOLD),
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # 🔹 centra el contenido
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        ),
        gradient=ft.LinearGradient(colors=[COLOR_ACCENT, "#145C70"]),
        width=180,
        height=45,
        border_radius=8,
        alignment=ft.alignment.center,  # 🔹 asegura centrado del contenedor
        ink=True,
        on_click=abrir_modal_instruccion,
    )

    modal_container = ft.Container(
        bgcolor=ft.Colors.with_opacity(0.65, "#000000"),
        expand=True,
        alignment=ft.alignment.center,
        visible=False,
        content=ft.Container(
            width=700,
            height=500,
            bgcolor="#0B1418",
            border_radius=12,
            border=ft.border.all(1, "#1E2C30"),
            padding=30,
            content=ft.Column(
                [
                    ft.Row([ft.Icon(ft.Icons.BOOK_OUTLINED, color=COLOR_ACCENT), modal_title], spacing=10),
                    ft.Row([btn_instruccion, ft.Text("Abrir plantilla recomendada", size=12, color="#AAAAAA")]),
                    text_area_syllabus,
                    ft.Row([btn_cancelar, btn_guardar], alignment=ft.MainAxisAlignment.END, spacing=10),
                ],
                spacing=15,
            ),
        ),
    )

    page.overlay.append(modal_container)
    page.overlay.append(modal_instruccion)

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
            modal_container,
            modal_instruccion,
        ],
        expand=True,
    )
