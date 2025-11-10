import flet as ft

def CursoDetalleView(page: ft.Page, curso_dict: dict, func_load_content):
    """
    Vista moderna y coherente con el resto del sistema dark-petróleo.
    """
    # ------------------------------------------------------
    # COLORES PRINCIPALES
    # ------------------------------------------------------
    COLOR_BG_CARD = "#0E1E25"
    COLOR_BG_CARD_HOVER = "#152B33"
    COLOR_BORDER_CARD = "#1F3A44"
    COLOR_ACCENT = "#1C8DB0"
    COLOR_TEXT_PRIMARY = "#EAEAEA"
    COLOR_TEXT_SECONDARY = "#AAB6B8"

    curso_nombre = curso_dict.get("curso", "Curso sin nombre")

    # ------------------------------------------------------
    # CABECERA
    # ------------------------------------------------------
    titulo_curso = ft.Text(
        curso_nombre,
        size=36,
        weight=ft.FontWeight.BOLD,
        color=COLOR_TEXT_PRIMARY,
    )

    btn_volver = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_color="#EAEAEA",
        icon_size=26,
        style=ft.ButtonStyle(
            shape=ft.CircleBorder(),
            bgcolor=ft.Colors.with_opacity(0.1, COLOR_ACCENT),
        ),
        tooltip="Volver",
        on_click=lambda e: func_load_content("Cursos"),
    )

    btn_home = ft.IconButton(
        icon=ft.Icons.HOME,
        icon_color="#EAEAEA",
        icon_size=26,
        style=ft.ButtonStyle(
            shape=ft.CircleBorder(),
            bgcolor=ft.Colors.with_opacity(0.1, COLOR_ACCENT),
        ),
        tooltip="Inicio",
        on_click=lambda e: page.go("/options"),
    )

    header = ft.Row(
        [titulo_curso, ft.Container(expand=True), btn_volver, btn_home],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # ------------------------------------------------------
    # BOTÓN DE MÓDULO REUTILIZABLE
    # ------------------------------------------------------
    def boton_modulo(texto, icono):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Text(
                        texto,
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color=COLOR_TEXT_PRIMARY,
                    ),
                    ft.Icon(icono, size=40, color=COLOR_ACCENT),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            width=500,
            height=110,
            border_radius=12,
            border=ft.border.all(1, COLOR_BORDER_CARD),
            bgcolor=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLOR_BG_CARD, "#0C252D"],
            ),
            padding=ft.padding.symmetric(horizontal=30, vertical=15),
            ink=True,
            animate=ft.Animation(180, "easeOut"),
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
            on_click=lambda e: func_load_content("Tareas", curso_dict)
            if texto == "Tareas"
            else func_load_content("Silabus", curso_dict),
        )

    # ------------------------------------------------------
    # BOTONES PRINCIPALES
    # ------------------------------------------------------
    btn_tareas = boton_modulo("Tareas", ft.Icons.CHECKLIST)
    btn_silabus = boton_modulo("Silabus", ft.Icons.DESCRIPTION)

    # ------------------------------------------------------
    # ESTRUCTURA PRINCIPAL
    # ------------------------------------------------------
    contenido = ft.Column(
        [
            header,
            ft.Container(height=50),
            btn_tareas,
            btn_silabus,
        ],
        spacing=30,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    layout = ft.Container(
        content=contenido,
        expand=True,
        alignment=ft.alignment.top_center,
        padding=ft.padding.all(50),
    )

    # ------------------------------------------------------
    # FONDO CON DEGRADADO COHERENTE
    # ------------------------------------------------------
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
