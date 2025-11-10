import flet as ft
from app.controllers.cursos_controller import crear_curso, obtener_cursos, actualizar_curso
from app.utils.vald_text_fields import validar_formulario
from app.controllers.aulas_controller import obtener_aula_by_id
from app.controllers.aulas_usuario_controller import obtener_miembros_de_aula
from app.utils.is_staff_verification import is_staff_verification


def contenedor_cursos(page: ft.Page, id_aula: int, func_load_content):
    edit_mode = False
    editing_course_id = None
    view_content = ft.Ref[ft.Container]()
    session_aula = page.session.get("selected_aula")
    session_aula_id = page.session.get("selected_aula_id")
    is_staff = is_staff_verification(page, id_aula)

    aula_actual = session_aula or (
        obtener_aula_by_id(int(session_aula_id)) if session_aula_id else None
    )

    aula_nombre = (
        (aula_actual.get("nombre_aula") if isinstance(aula_actual, dict) else None)
        or (aula_actual.get("nombre") if isinstance(aula_actual, dict) else None)
        or "Aula sin nombre"
    )

    # ------------------------------------------------------
    # 🔹 ESTILO UNIFICADO CON DASHBOARD
    # ------------------------------------------------------
    COLOR_BG_CARD = "#0E1E25"
    COLOR_BG_CARD_HOVER = "#152B33"
    COLOR_BORDER_CARD = "#1F3A44"
    COLOR_ACCENT = "#1C8DB0"
    COLOR_TEXT_PRIMARY = "#EAEAEA"
    COLOR_TEXT_SECONDARY = "#AAB6B8"

    # ------------------------------------------------------
    # 🔸 TARJETA DE CURSO
    # ------------------------------------------------------
    def course_card(curso_dict):
        nombre = curso_dict.get("curso")
        docente = curso_dict.get("docente")
        delegado = curso_dict.get("delegado")
        curso_id = curso_dict.get("id_curso")

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                nombre,
                                size=18,
                                weight=ft.FontWeight.W_500,
                                color=COLOR_TEXT_PRIMARY,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                icon_color=COLOR_TEXT_SECONDARY,
                                icon_size=20,
                                tooltip="Editar curso",
                                on_click=lambda e, c=curso_dict: abrir_modal_para_editar(c),
                                visible=is_staff,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Text(f"ID Curso: {curso_id}", color="#7C8B8C", size=12),
                    ft.Text(f"Docente: {docente}", color="#C7D3D4", size=14),
                    ft.Text(f"Delegado: {delegado}", color="#C7D3D4", size=14),
                ],
                spacing=6,
            ),
            width=320,
            height=150,
            border_radius=12,
            padding=15,
            border=ft.border.all(1, COLOR_BORDER_CARD),
            bgcolor=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLOR_BG_CARD, "#0C252D"],
            ),
            ink=True,
            on_hover=lambda e: (
                setattr(
                    e.control,
                    "bgcolor",
                    ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=[COLOR_BG_CARD_HOVER, "#133540"]
                    ) if e.data == "true" else
                    ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=[COLOR_BG_CARD, "#0C252D"]
                    ),
                ),
                e.control.update(),
            ),
            on_click=lambda e: func_load_content("Curso", curso_dict),
        )

    # ------------------------------------------------------
    # GRID DE CURSOS
    # ------------------------------------------------------
    def course_grid(cards, max_per_row=3):
        rows = [
            ft.Row(cards[i:i + max_per_row], spacing=20)
            for i in range(0, len(cards), max_per_row)
        ]
        return ft.Container(content=ft.Column(rows, spacing=20))

    # ------------------------------------------------------
    # MODAL DE CREAR / EDITAR
    # ------------------------------------------------------
    nombre_curso = ft.TextField(
        label="Nombre del Curso",
        bgcolor="#0D1A20",
        border_radius=8,
        border_color="#1F3A44",
        focused_border_color=COLOR_ACCENT,
        color=COLOR_TEXT_PRIMARY,
    )

    docente = ft.TextField(
        label="Docente",
        bgcolor="#0D1A20",
        border_radius=8,
        border_color="#1F3A44",
        focused_border_color=COLOR_ACCENT,
        color=COLOR_TEXT_PRIMARY,
    )

    try:
        miembros = obtener_miembros_de_aula(id_aula)
    except Exception:
        miembros = []

    delegado = ft.Dropdown(
        label="Delegado",
        options=[
            ft.dropdown.Option(str(m.get("id_usuario")),
                f"{m.get('nombre','').strip()} {m.get('apellido','').strip()}".strip())
            for m in miembros
        ],
        width=300,
    )

    modal_title = ft.Text("CREAR CURSO", weight=ft.FontWeight.BOLD, size=22, color="#FFFFFF")

    def validar_y_crear_curso(e):
        nonlocal edit_mode, editing_course_id
        if not validar_formulario(page, [nombre_curso, docente, delegado]):
            return
        delegado_id = int(delegado.value) if delegado.value else None
        if edit_mode:
            actualizar_curso(editing_course_id, nombre_curso.value, docente.value, delegado_id)
        else:
            crear_curso(id_aula, nombre_curso.value, docente.value, delegado_id)
        cerrar_modal(e)
        cargar_grid_cursos(id_aula)

    def abrir_modal_para_editar(curso_dict):
        nonlocal edit_mode, editing_course_id
        editing_course_id = curso_dict.get("id_curso")
        nombre_curso.value = curso_dict.get("curso")
        docente.value = curso_dict.get("docente") or ""
        delegado.value = str(curso_dict.get("id_delegado") or "")
        edit_mode = True
        modal_title.value = "EDITAR CURSO"
        abrir_modal(None)

    def abrir_modal(e):
        page.overlay.append(modal_container)
        modal_container.visible = True
        page.update()

    def cerrar_modal(e):
        nonlocal edit_mode, editing_course_id
        modal_container.visible = False
        if modal_container in page.overlay:
            page.overlay.remove(modal_container)
        edit_mode = False
        editing_course_id = None
        page.update()

    btn_guardar = ft.Container(
        content=ft.Text("Guardar", color="#FFFFFF", size=16, weight=ft.FontWeight.W_500),
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=[COLOR_ACCENT, "#145C70"],
        ),
        width=150,
        height=45,
        border_radius=8,
        alignment=ft.alignment.center,
        ink=True,
        on_click=validar_y_crear_curso,
    )

    btn_cancelar = ft.Container(
        content=ft.Text("Cancelar", color=COLOR_TEXT_SECONDARY, size=16),
        width=120,
        height=45,
        border_radius=8,
        alignment=ft.alignment.center,
        ink=True,
        border=ft.border.all(1, "#2C2C2C"),
        on_click=cerrar_modal,
    )

    form_container = ft.Container(
        width=700,
        height=400,
        bgcolor="#0B1418",
        border_radius=12,
        padding=30,
        border=ft.border.all(1, "#1E2C30"),
        content=ft.Column(
            [
                ft.Row([ft.Icon(ft.Icons.ADD_BOX_OUTLINED, color=COLOR_ACCENT), modal_title], spacing=10),
                nombre_curso, docente, delegado,
                ft.Container(height=15),
                ft.Row([btn_cancelar, btn_guardar],
                       alignment=ft.MainAxisAlignment.END, spacing=10),
            ],
            spacing=12,
        ),
    )

    modal_container = ft.Container(
        bgcolor=ft.Colors.with_opacity(0.65, "#000000"),
        expand=True,
        alignment=ft.alignment.center,
        content=form_container,
        visible=False,
    )

    # ------------------------------------------------------
    # HEADER
    # ------------------------------------------------------
    btn_volver = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_color="#EAEAEA",
        icon_size=26,
        style=ft.ButtonStyle(
            shape=ft.CircleBorder(),
            bgcolor=ft.Colors.with_opacity(0.1, "#1C8DB0"),
        ),
        tooltip="Volver",
        on_click=lambda e: page.go("/tus_aulas"),
    )

    btn_home = ft.IconButton(
        icon=ft.Icons.HOME,
        icon_color="#EAEAEA",
        icon_size=26,
        style=ft.ButtonStyle(
            shape=ft.CircleBorder(),
            bgcolor=ft.Colors.with_opacity(0.1, "#1C8DB0"),
        ),
        tooltip="Inicio",
        on_click=lambda e: page.go("/options"),
    )

    btn_add = ft.Container(
        content=ft.Row(
            [ft.Icon(ft.Icons.ADD, color="#FFFFFF"), ft.Text("Añadir curso", color="#FFFFFF")],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=6,
        ),
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=[COLOR_ACCENT, "#186678"],
        ),
        width=180,
        height=45,
        border_radius=8,
        ink=True,
        visible=is_staff,
        on_click=abrir_modal,
    )

    titulo = ft.Text(
        f"Cursos - {aula_nombre}",
        size=32,
        weight=ft.FontWeight.BOLD,
        color=COLOR_TEXT_PRIMARY,
    )

    header = ft.Row(
        [
            titulo,
            ft.Container(expand=True),
            btn_add,
            btn_volver,
            btn_home  # ← restaurado y rediseñado
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # ------------------------------------------------------
    # CONTENIDO PRINCIPAL
    # ------------------------------------------------------
    def cargar_grid_cursos(id_aula_cargada):
        cursos_list = obtener_cursos(id_aula_cargada)
        cards = [course_card(c) for c in cursos_list]
        grid = (
            ft.Container(
                content=ft.Text("No hay cursos creados en esta aula.", color="#AAAAAA"),
                alignment=ft.alignment.center,
                expand=True
            )
            if not cards else course_grid(cards, max_per_row=4)
        )
        if view_content.current:
            view_content.current.content = ft.Column(
                [header, grid],
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True,
            )
            page.update()

    cursos_list_inicial = obtener_cursos(id_aula)
    cards_iniciales = [course_card(c) for c in cursos_list_inicial]
    grid_inicial = (
        ft.Container(
            content=ft.Text("No hay cursos creados en esta aula.", color="#AAAAAA"),
            alignment=ft.alignment.center,
            expand=True,
        )
        if not cards_iniciales
        else course_grid(cards_iniciales, max_per_row=4)
    )

    main_content = ft.Column(
        [header, ft.Container(height=20), grid_inicial],
        scroll=ft.ScrollMode.ADAPTIVE,
        expand=True,
    )

    return ft.Stack(
        [
            ft.Container(ref=view_content, content=main_content, expand=True, padding=30),
            modal_container,
        ],
        expand=True,
    )
