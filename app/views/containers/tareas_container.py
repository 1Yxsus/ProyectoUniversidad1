import flet as ft
from app.utils.vald_text_fields import validar_formulario
from app.controllers.tareas_controller import crear_tarea, actualizar_tarea, obtener_tareas_por_curso
import datetime

def TareasCursoView(page: ft.Page, curso_dict: dict, selected_id: int, func_cursos_load):
    """
    Vista que muestra la lista de tareas de un curso con tarjetas personalizadas.
    """

    # ------------------------------------------------------
    # 2️⃣ ESTADOS Y VARIABLES INTERNAS
    # ------------------------------------------------------
    edit_mode = False
    editing_course_id = None
    selected_id = None

    # --- DATOS DEL CURSO ---
    curso_nombre = curso_dict.get("curso")

    # --- TÍTULO PRINCIPAL ---
    titulo_curso = ft.Text(
        curso_nombre,
        size=40,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE,
    )

    # --- SUBTÍTULO ---
    subtitulo = ft.Text(
        "TAREAS",
        size=24,
        weight=ft.FontWeight.BOLD,
        color="#C9C9C9",
    )

    # --- BOTÓN AÑADIR TAREA ---
    btn_añadir = ft.ElevatedButton(
        text="Añadir Tarea",
        icon=ft.Icons.ADD,
        bgcolor="#2A2A2A",
        color=ft.Colors.WHITE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
        ),
        on_click= lambda e: abrir_modal(e),
    )

    # ------------------------------------------------------
    # 6️⃣ COMPONENTES DEL MODAL CREAR/EDITAR CURSO
    # ------------------------------------------------------
    titulo = ft.TextField(label="Titulo:", bgcolor="#1E1E1E", border_radius=10)
    descripcion = ft.TextField(label="Descripción:", bgcolor="#1E1E1E", border_radius=10)
    publicado_por = ft.TextField(label="Nombre:", bgcolor="#1E1E1E", border_radius=10)
    fecha_limite = ft.TextField(label="Fecha Limite:", bgcolor="#1E1E1E", border_radius=10)


    # fecha_limite = ft.DatePicker(
    #     field_label_text="Fecha Límite:",
    #     first_date=datetime.time(2020, 1, 1),
    #     last_date=datetime.time(2030, 12, 31),
    #     on_change=lambda e: (
    #         setattr(fecha_limite, "value", str(fecha_limite.value.strftime("%d/%m/%Y"))),
    #         page.update()
    #     )
    # )

    modal_title = ft.Text("CREAR TAREA", weight=ft.FontWeight.BOLD, size=22, color=ft.Colors.WHITE)

    campos = [titulo, descripcion, publicado_por, fecha_limite]

    # Lógica para guardar
    print("Datos correctos ✅")

    def validar_y_crear_curso(e):
        nonlocal edit_mode, editing_course_id
        if not validar_formulario(page, campos):
            return
        
        # obtener fecha en formato ISO (o None)
        fecha_entrega_val = fecha_limite.value
        fecha_entrega_val = fecha_limite.value  # datetime.date o None
        fecha_entrega_str = fecha_entrega_val.isoformat() if fecha_entrega_val else None

        if edit_mode:
            actualizar_tarea(editing_course_id, titulo.value, descripcion.value, int(publicado_por.value))
        else:
            crear_tarea(curso_dict.get("id_curso"), titulo.value, descripcion.value, int(publicado_por.value))
            crear_tarea(curso_dict.get("id_curso"), titulo.value, descripcion.value, int(publicado_por.value), fecha_entrega_str)
        cerrar_modal(e)
        func_cursos_load(selected_id)

    def abrir_modal(e):
        modal_container.visible = True
        page.update()

    def cerrar_modal(e):
        nonlocal edit_mode, editing_course_id
        modal_container.visible = False
        titulo.value = descripcion.value = publicado_por.value = ""
        edit_mode = False
        editing_course_id = None
        modal_title.value = "CREAR CURSO"
        btn_crear_modal.text = "CREAR"
        page.update()

    btn_crear_modal = ft.ElevatedButton(text="CREAR", on_click=validar_y_crear_curso)
    btn_cancelar_modal = ft.TextButton(text="Cancelar", on_click=cerrar_modal)

    form_container = ft.Container(
        width=700,
        height=400,
        bgcolor="#121212",
        border_radius=12,
        padding=30,
        content=ft.Column(
            [
                ft.Row([ft.Icon(ft.Icons.ADD_BOX_OUTLINED), modal_title], spacing=10),
                titulo, descripcion, publicado_por, fecha_limite,
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


    # --- BOTÓN VOLVER ---
    btn_volver = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_color=ft.Colors.WHITE,
        icon_size=26,
        style=ft.ButtonStyle(
            shape=ft.CircleBorder(),
            bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
        ),
        tooltip="Volver",
        on_click=lambda e: func_cursos_load(selected_id),
    )

    # --- HEADER SUPERIOR ---
    header = ft.Row(
        [
            titulo_curso,
            ft.Container(expand=True),
            btn_añadir,
            btn_volver,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # --- COMPONENTE DE UNA TAREA ---
    def card_tarea(titulo="Titulo", descripcion="", fecha_limite="--/--/--", fecha_publicacion="--/--/--"):
        expanded = ft.Ref[bool]()
        expanded.current = False

        # Elementos de texto
        titulo_text = ft.Text(titulo, size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
        fecha_text = ft.Text(f"Fecha límite: {fecha_limite}", size=14, color="#CCCCCC")

        # Descripción y fecha de publicación
        descripcion_col = ft.Column(
            [
                ft.Text(descripcion, color="#CCCCCC", size=14),
                ft.Text(f"Fecha de Publicación: {fecha_publicacion}", size=13, color="#888888"),
            ],
            spacing=5,
            visible=False,
        )

        # Ícono desplegable
        icono = ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, color=ft.Colors.WHITE)

        # Al hacer clic, alterna expansión
        def toggle_expand(e):
            expanded.current = not expanded.current
            descripcion_col.visible = expanded.current
            icono.name = ft.Icons.KEYBOARD_ARROW_UP if expanded.current else ft.Icons.KEYBOARD_ARROW_DOWN
            tarjeta.update()

        # Estructura visual
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

    # --- LISTA DE TAREAS (de ejemplo) ---
    tareas_list = obtener_tareas_por_curso(curso_dict.get("id_curso"))

    lista_tareas = ft.Container(
        expand=True,  # <- toma todo el espacio disponible restante
        content=ft.Column(
            [card_tarea(t["titulo"], t["descripcion"], t["fecha_entrega"], t["fecha_publicacion"]) for t in tareas_list],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,  # ahora sí puede scrollear
            expand=True,
        ),
    )

    # --- ESTRUCTURA PRINCIPAL ---
    contenido = ft.Column(
        [
            header,
            ft.Container(height=30),
            subtitulo,
            ft.Container(height=20),
            lista_tareas,
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        expand=True,
    )

    # --- CONTAINER FINAL ---
    layout = ft.Container(
        content=ft.Stack([contenido, modal_container], expand=True),
        expand=True,
        alignment=ft.alignment.top_center,
        padding=ft.padding.all(40),
        bgcolor="#000000",
    )

    return layout
