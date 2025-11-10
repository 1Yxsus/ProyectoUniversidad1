import flet as ft


def HomeView(page: ft.Page):
    """
    Pantalla principal unificada con estilo dark-petróleo minimalista.
    """
    # ================================
    # COLORES BASE
    # ================================
    COLOR_ACCENT = "#1C8DB0"
    COLOR_BG_CARD = "#0E1E25"
    COLOR_BG_HOVER = "#152B33"
    COLOR_TEXT = "#EAEAEA"
    COLOR_TEXT_SEC = "#AAB6B8"

    page.bgcolor = "#000000"
    page.scroll = ft.ScrollMode.AUTO

    # ================================
    # ENCABEZADO PRINCIPAL
    # ================================
    titulo = ft.Text(
        "UniversApp",
        size=42,
        weight=ft.FontWeight.BOLD,
        color=COLOR_TEXT,
        text_align=ft.TextAlign.CENTER,
    )

    subtitulo = ft.Text(
        "Organiza, colabora y potencia tu productividad universitaria.\n"
        "Una plataforma creada por estudiantes, para estudiantes.",
        size=18,
        color=COLOR_TEXT_SEC,
        text_align=ft.TextAlign.CENTER,
        width=600,
    )

    # ================================
    # IMAGEN PRINCIPAL
    # ================================
    imagen_principal = ft.Image(
        src="assets/images/logo_main.png",
        width=320,
        height=320,
        fit=ft.ImageFit.CONTAIN,
    )

    # ================================
    # TARJETAS DE FUNCIONALIDAD
    # ================================
    def card_funcionalidad(icono, titulo, texto):
        return ft.Container(
            width=210,
            height=230,
            border_radius=18,
            border=ft.border.all(1, "#1F3A44"),
            bgcolor=ft.LinearGradient(colors=[COLOR_BG_CARD, "#0C252D"]),
            padding=15,
            ink=True,
            animate=ft.Animation(180, "easeOut"),
            on_hover=lambda e: (
                setattr(
                    e.control,
                    "bgcolor",
                    ft.LinearGradient(colors=[COLOR_BG_HOVER, "#133540"])
                    if e.data == "true"
                    else ft.LinearGradient(colors=[COLOR_BG_CARD, "#0C252D"]),
                ),
                e.control.update(),
            ),
            content=ft.Column(
                [
                    ft.Image(src=icono, width=90, height=90, fit=ft.ImageFit.CONTAIN),
                    ft.Text(
                        titulo,
                        size=15,
                        weight=ft.FontWeight.BOLD,
                        color=COLOR_TEXT,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        texto,
                        size=13,
                        color=COLOR_TEXT_SEC,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
        )

    seccion_funcionalidades = ft.Row(
        [
            card_funcionalidad(
                "assets/icons/horarios.png",
                "Organiza tus horarios",
                "Administra tus clases, reuniones y recordatorios en un solo lugar.",
            ),
            card_funcionalidad(
                "assets/icons/tareas.png",
                "Gestiona tus tareas",
                "Crea, asigna y revisa tus pendientes fácilmente.",
            ),
            card_funcionalidad(
                "assets/icons/anuncio.png",
                "Recibe anuncios",
                "Mantente al día con la información más importante de tus cursos.",
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=25,
        run_spacing=10,
        wrap=True,
    )

    # ================================
    # BOTÓN PRINCIPAL
    # ================================
    btn_empezar = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.PLAY_ARROW, color="#FFFFFF"),
                ft.Text("Comenzar ahora", color="#FFFFFF", size=16, weight=ft.FontWeight.BOLD),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        ),
        gradient=ft.LinearGradient(colors=[COLOR_ACCENT, "#145C70"]),
        width=220,
        height=50,
        border_radius=10,
        alignment=ft.alignment.center,
        ink=True,
        on_click=lambda e: page.go("/login"),
        animate=ft.Animation(200, "easeOut"),
        on_hover=lambda e: (
            setattr(
                e.control,
                "gradient",
                ft.LinearGradient(colors=["#23A5C8", "#17748C"])
                if e.data == "true"
                else ft.LinearGradient(colors=[COLOR_ACCENT, "#145C70"]),
            ),
            e.control.update(),
        ),
    )

    # ================================
    # CONTENIDO PRINCIPAL
    # ================================
    contenido = ft.Column(
        [
            titulo,
            subtitulo,
            ft.Container(height=15),
            imagen_principal,
            ft.Container(height=15),
            seccion_funcionalidades,
            ft.Container(height=40),
            btn_empezar,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15,
    )

    # ================================
    # FONDO GRADIENTE PETRÓLEO
    # ================================
    fondo = ft.Container(
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#0C1C24", "#0E2329", "#08171C"],
        ),
        content=ft.Container(
            content=contenido,
            alignment=ft.alignment.center,
            expand=True,
            padding=ft.padding.symmetric(horizontal=40, vertical=50),
        ),
        expand=True,
    )

    return fondo
