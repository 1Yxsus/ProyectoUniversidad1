import flet as ft

def AulaDashboardView(page: ft.Page):
    # --- Información de usuario ---
    user = page.session.get("user")

    if not user:
        page.go("/login")
        return

    id = user["id_usuario"]
    nombre = user["nombre"]
    apellido = user["apellido"]
    correo = user["correo"]
    fecha = user["fecha_registro"]



    # --- CONFIGURACIÓN GENERAL ---
    page.bgcolor = "#000000"
    page.title = "Aula 365 | Cursos"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # --- DESPLEGABLE DE AULA ---
    dropdown_aula = ft.Dropdown(
        value="Aula 365",
        options=[
            ft.dropdown.Option("Aula 365"),
            ft.dropdown.Option("Aula 202"),
            ft.dropdown.Option("Aula 101"),
        ],
        bgcolor="#111111",
        color=ft.Colors.WHITE,
        border_color="#333333",
        focused_border_color="#555555",
        width=150,
    )

    # --- USUARIO (ICONO Y NOMBRE) ---
    user_info = ft.Column(
        [
            ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=70, color=ft.Colors.WHITE),
            ft.Text(f"{nombre} {apellido}", size=20, color=ft.Colors.LIGHT_BLUE_ACCENT, weight=ft.FontWeight.W_500),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5,
    )

    # --- BOTONES DE MENÚ IZQUIERDO ---
    def side_button(text, route):
        return ft.Container(
            content=ft.Text(text, color=ft.Colors.WHITE, size=18),
            width=150,
            height=45,
            alignment=ft.alignment.center,
            bgcolor="#1B1B1B",
            border_radius=10,
            ink=True,
            on_click=lambda e: page.go(route),
        )

    btn_cursos = side_button("Cursos", "/cursos")
    btn_anuncios = side_button("Anuncios", "/anuncios")

    btn_logout = ft.Container(
        content=ft.Text("Cerrar Sesión", color=ft.Colors.WHITE, size=18),
        width=150,
        height=45,
        alignment=ft.alignment.center,
        bgcolor="#2B0000",
        border_radius=10,
        ink=True,
        on_click=lambda e: page.go("/login"),
    )

    # --- SIDEBAR COMPLETO ---
    sidebar = ft.Container(
        width=200,
        bgcolor="#0A0A0A",
        padding=20,
        content=ft.Column(
            [
                dropdown_aula,
                ft.Container(height=30),
                user_info,
                ft.Container(height=30),
                btn_cursos,
                btn_anuncios,
                ft.Container(expand=True),
                btn_logout,
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    # --- TARJETA DE CURSO ---
    def course_card(nombre="Nombre Del Curso"):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(nombre, size=18, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
                            ft.Icon(ft.Icons.EDIT, color=ft.Colors.WHITE, size=18),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Text("Docente: Apellido Nombre", color="#AAAAAA", size=14),
                    ft.Text("Delegado: Apellido Nombre", color="#AAAAAA", size=14),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=5,
            ),
            width=320,
            height=150,
            bgcolor="#1A1A1A",
            border_radius=12,
            padding=15,
            ink=True,
            on_click=lambda e: print(f"Abrir curso: {nombre}"),
        )

    # --- SIMULACIÓN DE GRID SIN WRAP ---
    # Creamos filas manualmente con Row dentro de un Column
    def course_grid(cards, max_per_row=3):
        rows = []
        for i in range(0, len(cards), max_per_row):
            fila = ft.Row(
                cards[i:i+max_per_row],
                spacing=20,
                alignment=ft.MainAxisAlignment.START,
            )
            rows.append(fila)

        return ft.Container(
            content=ft.Column(
                rows,
                spacing=20,
                alignment=ft.MainAxisAlignment.START,
            ),
        )

    # Creamos tarjetas
    cards = [
        course_card("Programación Aplicada"),
        course_card("Base de Datos"),
        course_card("Ingeniería de Software"),
        course_card("Algoritmos Avanzados"),
        course_card("Matemática Discreta"),
        course_card("Redes de Computadoras"),
    ]

    cursos_grid = course_grid(cards, max_per_row=3)

    # --- BOTÓN AÑADIR CURSO ---
    btn_add_curso = ft.ElevatedButton(
        text="Añadir Curso",
        icon=ft.Icons.ADD,
        bgcolor="#333333",
        color=ft.Colors.WHITE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
        ),
        on_click=lambda e: page.go("/nuevo_curso"),
    )

    # --- BOTÓN HOME ---
    btn_home = ft.IconButton(
        icon=ft.Icons.HOME,
        icon_size=30,
        icon_color=ft.Colors.WHITE,
        bgcolor="#111111",
        on_click=lambda e: page.go("/options"),
    )

    # --- HEADER (TÍTULO + BOTONES DERECHA) ---
    header = ft.Row(
        [
            ft.Text("Cursos", size=45, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Container(expand=True),
            btn_add_curso,
            btn_home,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # --- CONTENIDO CENTRAL ---
    content = ft.Container(
        expand=True,
        padding=30,
        content=ft.Column(
            [
                header,
                ft.Container(height=30),
                cursos_grid,
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
    )

    # --- ESTRUCTURA PRINCIPAL (SIDEBAR + CONTENIDO) ---
    layout = ft.Row(
        [
            sidebar,
            ft.VerticalDivider(width=1, color="#333333"),
            content,
        ],
        expand=True,
    )

    return layout
