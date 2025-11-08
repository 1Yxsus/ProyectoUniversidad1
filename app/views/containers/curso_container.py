import flet as ft

def CursoDetalleView(page: ft.Page, curso_dict: dict, func_load_content):
    """
    Vista de detalle del curso (TAREAS y SILABUS).
    """
    curso_nombre = curso_dict.get("curso")

    # --- Título del curso ---
    titulo_curso = ft.Text(
        curso_nombre,
        size=40,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE,
    )

    # --- Botón volver ---
    btn_volver = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_color=ft.Colors.WHITE,
        icon_size=28,
        style=ft.ButtonStyle(
            shape=ft.CircleBorder(),
            bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
        ),
        tooltip="Volver",
        on_click=lambda e: page.go("/aula_dashboard"),
    )

    # --- Botón home ---
    btn_home = ft.IconButton(
        icon=ft.Icons.HOME,
        icon_color=ft.Colors.WHITE,
        icon_size=28,
        style=ft.ButtonStyle(
            shape=ft.CircleBorder(),
            bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
        ),
        tooltip="Inicio",
        on_click=lambda e: page.go("/options"),
    )

    # --- Header superior ---
    header = ft.Row(
        [
            titulo_curso,
            ft.Container(expand=True),
            btn_volver,
            btn_home,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # --- Tarjeta de botón (reutilizable) ---
    def boton_modulo(texto, icono):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Text(
                        texto,
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                    ),
                    ft.Icon(icono, size=40, color=ft.Colors.WHITE),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            width=500,
            height=100,
            bgcolor="#151515",
            border=ft.border.all(1, "#2A2A2A"),
            border_radius=10,
            padding=ft.padding.symmetric(horizontal=30, vertical=10),
            ink=True,
            animate=ft.Animation(150, "easeOut"),
            on_hover=lambda e: (
                setattr(e.control, "bgcolor", "#1E1E1E" if e.data == "true" else "#151515"),
                e.control.update(),
            ),
            on_click=lambda e: func_load_content("Tareas", curso_dict) if texto == "Tareas" else func_load_content("Silabus", curso_dict), 
        )

    # --- Botones principales ---
    btn_tareas = boton_modulo("Tareas", ft.Icons.CHECKLIST)
    btn_silabus = boton_modulo("Silabus", ft.Icons.DESCRIPTION)

    # --- Estructura principal ---
    contenido = ft.Column(
        [
            header,
            ft.Container(height=40),
            btn_tareas,
            btn_silabus,
        ],
        spacing=25,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        expand=True,
    )

    # --- Contenedor final ---
    layout = ft.Container(
        content=contenido,
        expand=True,
        alignment=ft.alignment.top_center,
        padding=ft.padding.all(40),
        bgcolor="#000000",
    )

    return layout
