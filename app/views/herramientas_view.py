import flet as ft

def ToolsDashboardView(page: ft.Page):
    # --- CONFIGURACIÓN GENERAL ---
    page.title = "Aula 365 | Herramientas"
    page.bgcolor = "#000000"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # --- BOTÓN HOME (arriba a la derecha) ---
    btn_home = ft.IconButton(
        icon=ft.Icons.HOME,
        icon_size=28,
        icon_color=ft.Colors.WHITE,
        bgcolor="#111111",
        tooltip="Volver al inicio",
        on_click=lambda e: page.go("/options"),
    )

    # --- ENCABEZADO ---
    header = ft.Row(
        [
            ft.Container(expand=True),
            btn_home,
        ],
        alignment=ft.MainAxisAlignment.END,
    )

    # --- TÍTULO PRINCIPAL ---
    titulo = ft.Text(
        "Herramientas",
        size=45,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE,
    )

    # --- FUNCIÓN PARA TARJETAS ---
    def tool_card(icon, text, route=None, enabled=True):
        return ft.Container(
            width=260,
            height=160,
            bgcolor="#111111",
            border_radius=16,
            alignment=ft.alignment.center,
            border=ft.border.all(1, "#333333"),
            ink=True,
            on_click=(lambda e: page.go(route)) if enabled and route else None,
            content=ft.Column(
                [
                    ft.Icon(icon, size=60, color=ft.Colors.WHITE),
                    ft.Text(
                        text,
                        size=20,
                        color=ft.Colors.WHITE,
                        weight=ft.FontWeight.W_500,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
        )

    # --- TARJETAS ---
    promodoro_card = tool_card(ft.Icons.ACCESS_TIME, "Pomodoro", route="/pomodoro")
    proximo_card = tool_card(ft.Icons.FLAG_OUTLINED, "Proximamente", enabled=False)

    # --- CONTENEDOR DE TARJETAS ---
    cards_row = ft.Row(
        [promodoro_card, proximo_card],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=40,
    )

    # --- CONTENIDO PRINCIPAL ---
    content = ft.Column(
        [
            header,
            ft.Container(height=40),
            titulo,
            ft.Container(height=40),
            cards_row,
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    # --- ESTRUCTURA FINAL ---
    layout = ft.Container(
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[
                ft.Colors.BLACK,
                ft.Colors.with_opacity(0.97, ft.Colors.BLUE_GREY_900),
            ],
        ),
        expand=True,
        content=content,
        padding=ft.padding.all(30),
    )

    return layout
