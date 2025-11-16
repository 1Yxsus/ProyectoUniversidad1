import flet as ft
from app.utils.vald_text_fields import validar_formulario
from app.controllers.tareas_controller import crear_tarea, actualizar_tarea, obtener_tareas_por_curso_ordenadas
import datetime
from app.utils.is_staff_verification import is_staff_verification
from app.utils.show_succes import show_success


def TareasCursoView(page: ft.Page, curso_dict: dict, selected_id: int, func_cursos_load):
    """
    Vista estilizada dark-petróleo que muestra la lista de tareas del curso.
    """

    # ------------------------------------------------------
    # COLORES BASE
    # ------------------------------------------------------
    COLOR_BG_CARD = "#0E1E25"
    COLOR_BG_CARD_HOVER = "#152B33"
    COLOR_BORDER_CARD = "#1F3A44"
    COLOR_ACCENT = "#1C8DB0"
    COLOR_TEXT_PRIMARY = "#EAEAEA"
    COLOR_TEXT_SECONDARY = "#AAB6B8"

    # ------------------------------------------------------
    # DATOS Y USUARIO
    # ------------------------------------------------------
    user = page.session.get("user")
    if not user:
        page.go("/login")
        return

    curso_nombre = curso_dict.get("curso")
    is_staff = is_staff_verification(page, curso_dict.get("id_aula"))

    # ------------------------------------------------------
    # ENCABEZADO
    # ------------------------------------------------------
    titulo_curso = ft.Text(curso_nombre, size=36, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_PRIMARY)
    subtitulo = ft.Text("TAREAS", size=22, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_SECONDARY)

    btn_añadir = ft.Container(
        content=ft.Row(
            [ft.Icon(ft.Icons.ADD, color="#FFFFFF"), ft.Text("Añadir Tarea", color="#FFFFFF")],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=6,
        ),
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=[COLOR_ACCENT, "#145C70"],
        ),
        width=180,
        height=45,
        border_radius=8,
        ink=True,
        visible=is_staff,
        on_click=lambda e: abrir_modal(e),
    )

    btn_volver = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_color="#EAEAEA",
        icon_size=26,
        style=ft.ButtonStyle(shape=ft.CircleBorder(), bgcolor=ft.Colors.with_opacity(0.1, COLOR_ACCENT)),
        tooltip="Volver",
        on_click=lambda e: func_cursos_load("Cursos"),
    )

    header = ft.Row(
        [titulo_curso, ft.Container(expand=True), btn_añadir, btn_volver],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # ------------------------------------------------------
    # CAMPOS DEL MODAL
    # ------------------------------------------------------
    titulo = ft.TextField(
        label="Título:",
        bgcolor="#0D1A20",
        border_radius=8,
        border_color="#1F3A44",
        focused_border_color=COLOR_ACCENT,
        color=COLOR_TEXT_PRIMARY,
    )
    descripcion = ft.TextField(
        label="Descripción:",
        bgcolor="#0D1A20",
        border_radius=8,
        border_color="#1F3A44",
        focused_border_color=COLOR_ACCENT,
        color=COLOR_TEXT_PRIMARY,
        multiline=True,
        min_lines=2,
        max_lines=3,
    )

    publicado_por = ft.TextField(
        label="Publicador:",
        value=f"{user.get('nombre','')} {user.get('apellido','')}".strip(),
        bgcolor="#0D1A20",
        border_radius=8,
        border_color="#1F3A44",
        color=COLOR_TEXT_PRIMARY,
        read_only=True,
    )

    fecha_limite = ft.TextField(
        label="Fecha Límite:",
        bgcolor="#0D1A20",
        border_radius=8,
        border_color="#1F3A44",
        color=COLOR_TEXT_PRIMARY,
        read_only=True,
    )

    date_picker = ft.DatePicker(
        first_date=datetime.date(2023, 1, 1),
        last_date=datetime.date(2035, 12, 31),
        on_change=lambda e: (
            setattr(fecha_limite, "value", date_picker.value.strftime("%Y-%m-%d")),
            page.update(),
        ),
    )
    page.overlay.append(date_picker)

    def abrir_datepicker(e):
        if hasattr(date_picker, "pick_date"):
            date_picker.pick_date()
        else:
            date_picker.open = True
            page.update()

    btn_fecha = ft.IconButton(
        icon=ft.Icons.CALENDAR_MONTH,
        icon_color="#FFFFFF",
        bgcolor="#133540",
        tooltip="Seleccionar fecha",
        on_click=abrir_datepicker,
    )

    fila_fecha = ft.Row([fecha_limite, btn_fecha], spacing=10)
    modal_title = ft.Text("CREAR TAREA", weight=ft.FontWeight.BOLD, size=22, color=COLOR_TEXT_PRIMARY)

    campos = [titulo, descripcion, publicado_por, fecha_limite]
    edit_mode = False
    editing_course_id = None

    # ------------------------------------------------------
    # FUNCIONES DEL MODAL
    # ------------------------------------------------------
    def validar_y_crear_tarea(e):
        nonlocal edit_mode, editing_course_id
        if not validar_formulario(page, campos):
            return

        try:
            if edit_mode:
                actualizar_tarea(
                    editing_course_id,
                    titulo.value,
                    descripcion.value,
                    fecha_limite.value,
                    user.get("id_usuario"),
                )
            else:
                crear_tarea(
                    curso_dict.get("id_aula"),
                    curso_dict.get("id_curso"),
                    titulo.value,
                    descripcion.value,
                    fecha_limite.value,
                    user.get("id_usuario"),
                )

            cerrar_modal(e)
            func_cursos_load("Tareas", curso_dict)
            show_success(page, "✅ Tarea guardada correctamente")
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al guardar tarea: {ex}"))
            page.snack_bar.open = True

        page.update()

    def abrir_modal(e):
        modal_container.visible = True
        page.update()

    def cerrar_modal(e):
        nonlocal edit_mode, editing_course_id
        modal_container.visible = False
        edit_mode = False
        editing_course_id = None
        modal_title.value = "CREAR TAREA"
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
        on_click=validar_y_crear_tarea,
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
        height=450,
        bgcolor="#0B1418",
        border_radius=12,
        padding=30,
        border=ft.border.all(1, "#1E2C30"),
        content=ft.Column(
            [
                ft.Row([ft.Icon(ft.Icons.ADD_BOX_OUTLINED, color=COLOR_ACCENT), modal_title], spacing=10),
                titulo,
                descripcion,
                publicado_por,
                fila_fecha,
                ft.Container(height=15),
                ft.Row([btn_cancelar, btn_guardar], alignment=ft.MainAxisAlignment.END, spacing=10),
            ],
            spacing=12,
        ),
    )

    modal_container = ft.Container(
        bgcolor=ft.Colors.with_opacity(0.6, "#000000"),
        expand=True,
        alignment=ft.alignment.center,
        content=form_container,
        visible=False,
    )

    # ------------------------------------------------------
    # TARJETAS DE TAREAS
    # ------------------------------------------------------
    def card_tarea(titulo, descripcion, fecha_limite, fecha_publicacion):
        expanded = ft.Ref[bool]()
        expanded.current = False

        desc_col = ft.Column(
            [
                ft.Text(descripcion, color=COLOR_TEXT_SECONDARY, size=14),
                ft.Text(f"Publicado: {fecha_publicacion}", size=12, color="#6F8C8D"),
            ],
            spacing=5,
            visible=False,
        )
        icono = ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, color=COLOR_TEXT_PRIMARY)

        def toggle_expand(e):
            expanded.current = not expanded.current
            desc_col.visible = expanded.current
            icono.name = ft.Icons.KEYBOARD_ARROW_UP if expanded.current else ft.Icons.KEYBOARD_ARROW_DOWN
            tarjeta.update()

        tarjeta = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(titulo, size=18, weight=ft.FontWeight.W_600, color=COLOR_TEXT_PRIMARY),
                            ft.Container(expand=True),
                            ft.Text(f"Entrega: {fecha_limite}", color="#98B8B9", size=13),
                            ft.IconButton(icon=icono.name, icon_color=COLOR_TEXT_PRIMARY, on_click=toggle_expand),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    desc_col,
                ],
                spacing=6,
            ),
            border_radius=10,
            border=ft.border.all(1, COLOR_BORDER_CARD),
            bgcolor=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLOR_BG_CARD, "#0C252D"],
            ),
            padding=ft.padding.all(15),
            ink=True,
            on_hover=lambda e: (
                setattr(
                    e.control,
                    "bgcolor",
                    ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=[COLOR_BG_CARD_HOVER, "#133540"],
                    )
                    if e.data == "true"
                    else ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=[COLOR_BG_CARD, "#0C252D"],
                    ),
                ),
                e.control.update(),
            ),
        )
        return tarjeta

    # ------------------------------------------------------
    # LISTA DE TAREAS
    # ------------------------------------------------------
    tareas_list = obtener_tareas_por_curso_ordenadas(curso_dict.get("id_curso"))
    lista_tareas = ft.Column(
        [card_tarea(t["titulo"], t["descripcion"], t["fecha_entrega"], t["fecha_publicacion"]) for t in tareas_list],
        spacing=15,
        scroll=ft.ScrollMode.ADAPTIVE,
        expand=True,
    )

    # ------------------------------------------------------
    # ESTRUCTURA FINAL
    # ------------------------------------------------------
    contenido = ft.Column(
        [header, ft.Container(height=25), subtitulo, ft.Container(height=10), lista_tareas],
        spacing=20,
        expand=True,
    )

    layout = ft.Container(
        content=ft.Stack([contenido, modal_container], expand=True),
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
        ],
        expand=True,
    )
