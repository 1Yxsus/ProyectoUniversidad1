import flet as ft
from app.utils.vald_text_fields import validar_formulario
from app.controllers.tareas_controller import crear_tarea, actualizar_tarea, obtener_tareas_por_curso_ordenadas
import datetime


def TareasCursoView(page: ft.Page, curso_dict: dict, selected_id: int, func_cursos_load):
    """
    Vista que muestra la lista de tareas de un curso con tarjetas personalizadas.
    """

    # ------------------------------------------------------
    # VARIABLES INTERNAS
    # ------------------------------------------------------

    user = page.session.get("user")

    if not user:
        page.go("/login")
        return

    edit_mode = False
    editing_course_id = None

    curso_nombre = curso_dict.get("curso")

    # ------------------------------------------------------
    # ENCABEZADO
    # ------------------------------------------------------
    titulo_curso = ft.Text(curso_nombre, size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
    subtitulo = ft.Text("TAREAS", size=24, weight=ft.FontWeight.BOLD, color="#C9C9C9")

    # Botón Añadir Tarea
    btn_añadir = ft.ElevatedButton(
        text="Añadir Tarea",
        icon=ft.Icons.ADD,
        bgcolor="#2A2A2A",
        color=ft.Colors.WHITE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
        ),
        on_click=lambda e: abrir_modal(e),
    )

    # ------------------------------------------------------
    # CAMPOS DEL MODAL
    # ------------------------------------------------------
    titulo = ft.TextField(label="Título:", bgcolor="#1E1E1E", border_radius=10)
    descripcion = ft.TextField(label="Descripción:", bgcolor="#1E1E1E", border_radius=10)

    publicado_por_id = user.get("id_usuario")  # int o None

    # si prefieres mostrar nombre en el formulario, muestra nombre pero no lo envíes a la BD
    publicado_por = ft.TextField(
        label="Publicador:",
        value=f"{user.get('nombre','')} {user.get('apellido','')}".strip(),
        bgcolor="#1E1E1E",
        border_radius=10,
        read_only=True,  # evitar que el usuario escriba un id inválido
    )

    # --- Campo de Fecha (tipo DATE) ---
    fecha_limite = ft.TextField(
        label="Fecha Límite:",
        bgcolor="#1E1E1E",
        border_radius=10,
        color=ft.Colors.WHITE,
        read_only=True,  # No editable manualmente
    )

    # DatePicker agregado al overlay
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
        # Compatibilidad según versión de Flet
        if hasattr(date_picker, "pick_date"):
            date_picker.pick_date()
        else:
            date_picker.open = True
            page.update()

    btn_fecha = ft.IconButton(
        icon=ft.Icons.CALENDAR_MONTH,
        icon_color=ft.Colors.WHITE,
        bgcolor="#1A1A1A",
        tooltip="Seleccionar fecha",
        on_click=abrir_datepicker,
    )

    fila_fecha = ft.Row([fecha_limite, btn_fecha], spacing=10)

    modal_title = ft.Text("CREAR TAREA", weight=ft.FontWeight.BOLD, size=22, color=ft.Colors.WHITE)

    campos = [titulo, descripcion, publicado_por, fecha_limite]

    # ------------------------------------------------------
    # FUNCIONES DEL MODAL
    # ------------------------------------------------------
    def validar_y_crear_tarea(e):
        nonlocal edit_mode, editing_course_id
        if not validar_formulario(page, campos):
            return

        fecha_entrega_str = fecha_limite.value or None

        # usar id del usuario en la sesión; validar existencia
        if not publicado_por_id:
            page.snack_bar = ft.SnackBar(ft.Text("Error: usuario no autenticado."))
            page.snack_bar.open = True
            page.update()
            return

        try:
            if edit_mode:
                actualizar_tarea(editing_course_id, titulo.value, descripcion.value, fecha_entrega_str, publicado_por_id)
            else:
                crear_tarea(
                    curso_dict.get("id_curso"),
                    titulo.value,
                    descripcion.value,
                    fecha_entrega_str,
                    publicado_por_id,
                )
        except Exception as ex:
            # captura errores de integridad (FK) u otros y los muestra al usuario
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al guardar tarea: {ex}"))
            page.snack_bar.open = True
            page.update()
            return

        cerrar_modal(e)
        func_cursos_load("Tareas", curso_dict)  # recarga la vista de curso para actualizar la lista
        page.snack_bar = ft.SnackBar(ft.Text("✅ Tarea creada exitosamente"))
        page.snack_bar.open = True
        page.update()

    def abrir_modal(e):
        modal_container.visible = True
        page.update()

    def cerrar_modal(e):
        nonlocal edit_mode, editing_course_id
        modal_container.visible = False
        titulo.value = descripcion.value = publicado_por.value = fecha_limite.value = ""
        edit_mode = False
        editing_course_id = None
        modal_title.value = "CREAR TAREA"
        btn_crear_modal.text = "CREAR"
        page.update()

    btn_crear_modal = ft.ElevatedButton(text="CREAR", on_click=validar_y_crear_tarea)
    btn_cancelar_modal = ft.TextButton(text="Cancelar", on_click=cerrar_modal)

    form_container = ft.Container(
        width=700,
        height=420,
        bgcolor="#121212",
        border_radius=12,
        padding=30,
        content=ft.Column(
            [
                ft.Row([ft.Icon(ft.Icons.ADD_BOX_OUTLINED), modal_title], spacing=10),
                titulo,
                descripcion,
                publicado_por,
                fila_fecha,
                ft.Row([btn_cancelar_modal, btn_crear_modal], alignment=ft.MainAxisAlignment.END),
            ],
            spacing=10,
        ),
    )

    modal_container = ft.Container(
        bgcolor=ft.Colors.with_opacity(0.6, ft.Colors.BLACK),
        expand=True,
        alignment=ft.alignment.center,
        content=form_container,
        visible=False,
    )

    # ------------------------------------------------------
    # HEADER SUPERIOR
    # ------------------------------------------------------
    btn_volver = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_color=ft.Colors.WHITE,
        icon_size=26,
        style=ft.ButtonStyle(
            shape=ft.CircleBorder(),
            bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
        ),
        tooltip="Volver",
        on_click=lambda e: func_cursos_load("Cursos"),
    )

    header = ft.Row(
        [titulo_curso, ft.Container(expand=True), btn_añadir, btn_volver],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # ------------------------------------------------------
    # TARJETAS DE TAREAS
    # ------------------------------------------------------
    def card_tarea(titulo="Titulo", descripcion="", fecha_limite="--/--/--", fecha_publicacion="--/--/--"):
        expanded = ft.Ref[bool]()
        expanded.current = False

        titulo_text = ft.Text(titulo, size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
        fecha_text = ft.Text(f"Fecha límite: {fecha_limite}", size=14, color="#CCCCCC")

        descripcion_col = ft.Column(
            [
                ft.Text(descripcion, color="#CCCCCC", size=14),
                ft.Text(f"Fecha de Publicación: {fecha_publicacion}", size=13, color="#888888"),
            ],
            spacing=5,
            visible=False,
        )

        icono = ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, color=ft.Colors.WHITE)

        def toggle_expand(e):
            expanded.current = not expanded.current
            descripcion_col.visible = expanded.current
            icono.name = ft.Icons.KEYBOARD_ARROW_UP if expanded.current else ft.Icons.KEYBOARD_ARROW_DOWN
            tarjeta.update()

        tarjeta = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            titulo_text,
                            ft.Container(expand=True),
                            fecha_text,
                            ft.IconButton(
                                icon=icono.name,
                                icon_color=ft.Colors.WHITE,
                                icon_size=24,
                                on_click=toggle_expand,
                                style=ft.ButtonStyle(
                                    shape=ft.CircleBorder(),
                                    bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE),
                                ),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    descripcion_col,
                ],
                spacing=8,
            ),
            bgcolor="#151515",
            border_radius=10,
            padding=ft.padding.all(15),
            border=ft.border.all(1, "#333333"),
            ink=True,
            animate=ft.Animation(150, "easeOut"),
            on_hover=lambda e: (
                setattr(e.control, "bgcolor", "#1E1E1E" if e.data == "true" else "#151515"),
                e.control.update(),
            ),
        )

        return tarjeta

    # ------------------------------------------------------
    # LISTA DE TAREAS
    # ------------------------------------------------------
    tareas_list = obtener_tareas_por_curso_ordenadas(curso_dict.get("id_curso"))

    lista_tareas = ft.Container(
        expand=True,
        content=ft.Column(
            [card_tarea(t["titulo"], t["descripcion"], t["fecha_entrega"], t["fecha_publicacion"]) for t in tareas_list],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        ),
    )

    # ------------------------------------------------------
    # LAYOUT FINAL
    # ------------------------------------------------------
    contenido = ft.Column(
        [header, ft.Container(height=30), subtitulo, ft.Container(height=20), lista_tareas],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        expand=True,
    )

    layout = ft.Container(
        content=ft.Stack([contenido, modal_container], expand=True),
        expand=True,
        alignment=ft.alignment.top_center,
        padding=ft.padding.all(40),
        bgcolor="#000000",
    )

    return layout
