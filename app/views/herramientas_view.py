import flet as ft

def ToolsDashboardView(page: ft.Page):
    """
    Vista del panel de herramientas con estilo dark-petróleo medio unificado.
    """
    # ================================
    # COLORES BASE
    # ================================
    COLOR_ACCENT = "#1C8DB0"
    COLOR_BG_CARD = "#141C22"
    COLOR_BG_HOVER = "#1D2A31"
    COLOR_TEXT = "#E8EAEA"
    COLOR_TEXT_SEC = "#AAB6B8"

    # ================================
    # CONFIGURACIÓN GENERAL
    # ================================
    page.title = "UniRed - Herramientas"
    page.bgcolor = "#000000"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # ================================
    # BOTÓN HOME
    # ================================
    btn_home = ft.IconButton(
        icon=ft.Icons.HOME,
        icon_size=28,
        icon_color=ft.Colors.WHITE,
        tooltip="Volver al inicio",
        style=ft.ButtonStyle(
            shape=ft.CircleBorder(),
            bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
        ),
        on_click=lambda e: page.go("/options"),
    )

    # ================================
    # ENCABEZADO
    # ================================
    header = ft.Row(
        [ft.Container(expand=True), btn_home],
        alignment=ft.MainAxisAlignment.END,
    )

    # ================================
    # TÍTULO PRINCIPAL
    # ================================
    titulo = ft.Text(
        "Herramientas",
        size=44,
        weight=ft.FontWeight.BOLD,
        color=COLOR_TEXT,
    )

    subtitulo = ft.Text(
        "Optimiza tu estudio con herramientas diseñadas para la productividad.",
        size=16,
        color=COLOR_TEXT_SEC,
        text_align=ft.TextAlign.CENTER,
    )

    # ================================
    # FUNCIÓN PARA TARJETAS
    # ================================
    def tool_card(icon, text, route=None, enabled=True):
        base_color = COLOR_BG_CARD if enabled else "#1A1A1A"
        icon_color = COLOR_ACCENT if enabled else "#777777"
        text_color = COLOR_TEXT if enabled else "#777777"

        return ft.Container(
            width=260,
            height=170,
            bgcolor=base_color,
            border_radius=14,
            border=ft.border.all(1, "#243238"),
            shadow=ft.BoxShadow(
                spread_radius=0.5,
                blur_radius=12,
                color=ft.Colors.with_opacity(0.25, "#000000"),
                offset=ft.Offset(0, 4),
            ),
            alignment=ft.alignment.center,
            ink=True,
            on_click=(lambda e: page.go(route)) if enabled and route else None,
            animate=ft.Animation(250, "easeOut"),
            on_hover=lambda e: (
                setattr(
                    e.control,
                    "bgcolor",
                    COLOR_BG_HOVER if e.data == "true" else base_color,
                ),
                setattr(
                    e.control,
                    "shadow",
                    ft.BoxShadow(
                        blur_radius=18 if e.data == "true" else 12,
                        color=ft.Colors.with_opacity(
                            0.4 if e.data == "true" else 0.25, "#000000"
                        ),
                        offset=ft.Offset(0, 6 if e.data == "true" else 4),
                    ),
                ),
                e.control.update(),
            ),
            content=ft.Column(
                [
                    ft.Icon(icon, size=65, color=icon_color),
                    ft.Text(
                        text,
                        size=20,
                        color=text_color,
                        weight=ft.FontWeight.W_500,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
        )

    # ================================
    # TARJETAS DE HERRAMIENTAS
    # ================================
    promodoro_card = tool_card(ft.Icons.ACCESS_TIME, "Pomodoro", route="/pomodoro")
    proximo_card = tool_card(ft.Icons.FLAG_OUTLINED, "Próximamente", enabled=False)

    # ================================
    # CONTENEDOR DE TARJETAS
    # ================================
    cards_row = ft.Row(
        [promodoro_card, proximo_card],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=40,
    )

    # ================================
    # CONTENIDO PRINCIPAL
    # ================================
    content = ft.Column(
        [
            header,
            ft.Container(height=40),
            titulo,
            ft.Container(height=10),
            subtitulo,
            ft.Container(height=50),
            cards_row,
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    # ================================
    # ESTRUCTURA FINAL
    # ================================
    layout = ft.Container(
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[
                "#0A161B",
                "#0E2329",
                "#08171C",
            ],
        ),
        expand=True,
        content=content,
        padding=ft.padding.all(40),
    )

    return layout
