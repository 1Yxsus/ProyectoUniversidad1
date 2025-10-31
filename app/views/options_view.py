import flet as ft

def DashboardOptionsView(page: ft.Page):

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
    # contrasena = user["contrasena"]


    # --- CONFIGURACIÓN GENERAL ---
    page.bgcolor = "#000000"  # Negro total
    page.title = "Panel Principal"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # --- BOTÓN DE CERRAR SESIÓN ---
    btn_logout = ft.TextButton(
        text="Cerrar Sesión",
        style=ft.ButtonStyle(
            bgcolor="#2B0000",  # Rojo oscuro
            color=ft.Colors.WHITE,
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
        on_click=lambda e: page.go("/login"),
    )

    logout_container = ft.Container(
        content=btn_logout,
        padding=ft.padding.only(right=40, top=10),  # separa del borde
    )

    # --- TÍTULO BIENVENIDA ---
    lbl_bienvenida = ft.Text(
        value=f"Bienvenido, {nombre} {apellido}",
        size=40,
        color=ft.Colors.WHITE,
        weight=ft.FontWeight.W_500,
        italic=True,
        text_align=ft.TextAlign.CENTER,
    )

    # --- TextFields del modal ---
    nombre_aula = ft.TextField(
        label="Nombre del Aula:",
        hint_text="Ejemplo: AULA 203",
        bgcolor="#1E1E1E",
        border_radius=10,
    )

    descripcion = ft.TextField(
        label="Descripción:",
        hint_text="Máximo 200 caracteres",
        bgcolor="#1E1E1E",
        border_radius=10,
        multiline=True,
    )

    # --- Botón dentro del modal ---
    btn_crear_modal = ft.ElevatedButton(
        text="CREAR",
        bgcolor="#2C2F3A",
        color=ft.Colors.WHITE,
        width=200,
        height=60,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        on_click=lambda e: None,  # Simula acción
    )

    # --- Modal (Dialogo) ---
    dialogo_crear = ft.AlertDialog(
        modal=True,
        bgcolor="#121212",
        shape=ft.RoundedRectangleBorder(radius=10),
        title=ft.Row(
            [
                ft.Icon(ft.Icons.ADD_BOX_OUTLINED, color=ft.Colors.WHITE),
                ft.Text("CREAR AULA", weight=ft.FontWeight.BOLD, size=22),
            ],
            spacing=10,
        ),
        content=ft.Column(
            [
                ft.Text("Nombre del Aula:", weight=ft.FontWeight.BOLD),
                nombre_aula,
                ft.Text("Descripción:", weight=ft.FontWeight.BOLD),
                descripcion,
            ],
            tight=True,
            spacing=10,
        ),
        actions=[
            btn_crear_modal
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def abrir_modal(e):
        page.dialog = dialogo_crear
        dialogo_crear.open = True
        page.update()

    def crear_aula(e):
        dialogo_crear.open = False
        page.snack_bar.content = ft.Text("Aula creada")
        page.snack_bar.open = True
        page.update()

    btn_crear_modal.on_click = crear_aula

    # --- FUNCIÓN PARA CREAR BOTONES ---
    def create_button(icon, text, width=350, height=220, on_click=None):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, size=80, color=ft.Colors.WHITE),
                    ft.Text(text, size=28, color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor="#111111",  # Negro muy oscuro
            width=width,
            height=height,
            border_radius=15,
            alignment=ft.alignment.center,
            ink=True,
            on_click=on_click,
            border=ft.border.all(1, "#222222"),
        )

    # --- BOTONES IZQUIERDA Y DERECHA ---
    btn_crear_aula = create_button(ft.Icons.ADD, "Crear Aula", on_click=abrir_modal)
    btn_tus_aulas = create_button(ft.Icons.GROUP, "Tus Aulas", on_click=lambda e: page.go("/aula_dashboard"))
    # El botón de Herramientas ocupa el doble de alto
    btn_herramientas = create_button(
        ft.Icons.SETTINGS,
        "Herramientas",
        height=(220 * 2) + 20,  # alto de dos botones más espacio
        on_click=lambda e: page.go("/herramientas"),
        width=350,
    )

    # --- LAYOUT DE BOTONES ---
    botones = ft.Row(
        [
            ft.Column(
                [btn_crear_aula, btn_tus_aulas],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            btn_herramientas,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=40,
    )

    # --- CABECERA ---
    header = ft.Row(
        [
            ft.Container(expand=True),
            logout_container,
        ],
        alignment=ft.MainAxisAlignment.END,
    )

    # --- CONTENEDOR PRINCIPAL ---
    contenido = ft.Column(
        [
            header,
            lbl_bienvenida,
            ft.Container(height=30),
            botones,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    return ft.Container(
        content=contenido,
        alignment=ft.alignment.center,  # 👈 centra vertical y horizontal
        expand=True,                    # ocupa toda la pantalla
        bgcolor=ft.Colors.BLACK
    )
