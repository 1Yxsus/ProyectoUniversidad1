import flet as ft


def HomeView(page: ft.Page):
    page.bgcolor = ft.Colors.BLACK
    page.scroll = ft.ScrollMode.AUTO

    # --- Encabezado principal ---
    titulo = ft.Text(
        "Herramienta Univeritaria",
        size=40,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE,
        text_align=ft.TextAlign.CENTER,
    )

    subtitulo = ft.Text(
        "Organiza, colabora y potencia tu productividad universitaria.\nUna plataforma creada por estudiantes, para estudiantes.",
        size=17,
        color=ft.Colors.GREY_400,
        text_align=ft.TextAlign.CENTER,
        width=600,
    )

    # --- Imagen principal ---
    imagen_principal = ft.Image(
        src="assets/images/logo_main.png",  # 900x900
        width=320,
        height=320,
        fit=ft.ImageFit.CONTAIN,
    )

    # --- Funcionalidades (más compactas) ---
    def card_funcionalidad(icono, titulo, texto):
        return ft.Container(
            width=210,
            height=230,
            bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.WHITE),
            border_radius=20,
            padding=15,
            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.1, ft.Colors.WHITE)),
            content=ft.Column(
                [
                    ft.Image(src=icono, width=90, height=90, fit=ft.ImageFit.CONTAIN),
                    ft.Text(
                        titulo,
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        texto,
                        size=12.5,
                        color=ft.Colors.GREY_400,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
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
        spacing=25,  # 🔹 Más compacto
        run_spacing=10,
        wrap=True,
    )

    # --- Botón principal (más visible y cerca del contenido) ---
    btn_empezar = ft.ElevatedButton(
        text="Comenzar ahora",
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_500,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=14),
            elevation=6,
            padding=ft.padding.symmetric(horizontal=40, vertical=18),
        ),
        on_click=lambda e: page.go("/login"),
    )

    # --- Contenido principal centrado ---
    contenido = ft.Column(
        [
            titulo,
            subtitulo,
            ft.Container(height=25),
            imagen_principal,
            ft.Container(height=35),
            seccion_funcionalidades,
            ft.Container(height=40),
            btn_empezar,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15,
    )

    # --- Fondo con degradado sutil ---
    fondo = ft.Container(
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[
                ft.Colors.BLACK,
                ft.Colors.with_opacity(0.97, ft.Colors.BLUE_GREY_900),
            ],
        ),
        content=ft.Container(
            content=contenido,
            alignment=ft.alignment.center,
            expand=True,
            padding=ft.padding.symmetric(horizontal=40, vertical=30),
        ),
        expand=True,
    )

    return fondo
