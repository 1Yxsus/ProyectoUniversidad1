import flet as ft


def HomeView(page: ft.Page):
    # Encabezado principal
    titulo = ft.Text(
        "",
        size=32,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE,
        text_align=ft.TextAlign.CENTER,
    )

    subtitulo = ft.Text(
        "Una plataforma diseñada para mejorar la organización, la comunicación y la productividad de los estudiantes universitarios.",
        size=16,
        color=ft.Colors.GREY_300,
        text_align=ft.TextAlign.CENTER,
        width=600,
    )

    # Imagen principal de presentación (puedes colocar la ruta o URL)
    imagen_principal = ft.Image(
        src="assets/images/logo.jpg",  # 👈 cambia aquí
        width=450,
        height=250,
        fit=ft.ImageFit.CONTAIN,
    )

    # Sección con imágenes y descripciones breves
    seccion_funcionalidades = ft.Row(
        [
            ft.Column(
                [
                    ft.Image(src="RUTA/IMAGEN_HORARIOS.png", width=150, height=150),
                    ft.Text(
                        "Organiza tus horarios",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "Administra tus clases, reuniones y recordatorios en un solo lugar.",
                        size=12,
                        color=ft.Colors.GREY_300,
                        text_align=ft.TextAlign.CENTER,
                        width=180,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            ft.Column(
                [
                    ft.Image(src="RUTA/IMAGEN_TAREAS.png", width=150, height=150),
                    ft.Text(
                        "Gestiona tus tareas",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "Crea, asigna y revisa tus pendientes fácilmente.",
                        size=12,
                        color=ft.Colors.GREY_300,
                        text_align=ft.TextAlign.CENTER,
                        width=180,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            ft.Column(
                [
                    ft.Image(src="RUTA/IMAGEN_ANUNCIOS.png", width=150, height=150),
                    ft.Text(
                        "Recibe anuncios",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "Mantente al día con la información más importante de tus cursos.",
                        size=12,
                        color=ft.Colors.GREY_300,
                        text_align=ft.TextAlign.CENTER,
                        width=180,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=40,
    )

    # Botón de acción principal
    btn_empezar = ft.ElevatedButton(
        text="Comenzar ahora",
        bgcolor=ft.Colors.BLUE_500,
        color=ft.Colors.WHITE,
        on_click=lambda e: page.go("/login"),
        width=200,
        height=45,
    )

    # Columna principal
    contenido = ft.Column(
        [
            titulo,
            ft.Container(height=10),
            subtitulo,
            ft.Container(height=30),
            imagen_principal,
            ft.Container(height=40),
            seccion_funcionalidades,
            ft.Container(height=50),
            btn_empezar,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
    )

    # Contenedor centrado y expandido
    return ft.Container(
        content=contenido,
        alignment=ft.alignment.center,
        expand=True,
        bgcolor=ft.Colors.BLACK,
    )