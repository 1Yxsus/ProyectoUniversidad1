import flet as ft
from app.controllers.aulas_controller import crear_aulas
from app.utils.vald_text_fields import validar_formulario
from app.utils.show_succes import show_success


def DashboardOptionsView(page: ft.Page):
    # ================================
    # INFORMACIÓN DE USUARIO
    # ================================
    user = page.session.get("user")
    if not user:
        page.go("/login")
        return

    id = user["id_usuario"]
    nombre = user["nombre"]
    apellido = user["apellido"]

    # ================================
    # CONFIGURACIÓN GENERAL
    # ================================
    COLOR_ACCENT = "#1C8DB0"
    COLOR_BG_CARD = "#0E1E25"
    COLOR_BG_HOVER = "#152B33"
    COLOR_TEXT = "#EAEAEA"
    COLOR_TEXT_SEC = "#9FAEB1"

    page.bgcolor = "#000000"
    page.title = "Panel Principal"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # ================================
    # BOTÓN CERRAR SESIÓN
    # ================================
    btn_logout = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.LOGOUT, color="#FFFFFF"),
                ft.Text("Cerrar sesión", color="#FFFFFF", size=14, weight=ft.FontWeight.W_500),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=6,
        ),
        gradient=ft.LinearGradient(colors=["#A93226", "#7B1F1F"]),
        width=160,
        height=40,
        border_radius=10,
        alignment=ft.alignment.center,
        ink=True,
        on_click=lambda e: page.go("/login"),
    )

    logout_container = ft.Container(padding=ft.padding.only(right=40, top=20), content=btn_logout)

    # ================================
    # TÍTULO DE BIENVENIDA
    # ================================
    lbl_bienvenida = ft.Text(
        value=f"Bienvenido, {nombre} {apellido}",
        size=38,
        color=COLOR_TEXT,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    # ================================
    # CAMPOS DE MODAL
    # ================================
    nombre_aula = ft.TextField(
        label="Nombre del Aula:",
        hint_text="Ejemplo: AULA 203",
        bgcolor="#0D1A20",
        border_radius=8,
        border_color="#1F3A44",
        focused_border_color=COLOR_ACCENT,
        color=COLOR_TEXT,
    )

    descripcion = ft.TextField(
        label="Descripción:",
        hint_text="Máximo 200 caracteres",
        bgcolor="#0D1A20",
        border_radius=8,
        border_color="#1F3A44",
        focused_border_color=COLOR_ACCENT,
        color=COLOR_TEXT,
        multiline=True,
    )

    # ================================
    # FUNCIONES MODAL
    # ================================
    def abrir_modal(e):
        modal_container.visible = True
        page.update()

    def cerrar_modal(e):
        modal_container.visible = False
        nombre_aula.value = ""
        descripcion.value = ""
        nombre_aula.error_text = None
        descripcion.error_text = None
        page.update()

    def crear_aula_action(e):
        if not validar_formulario(page, [nombre_aula, descripcion], "Por favor, completa todos los campos."):
            return

        success, msg = crear_aulas(nombre_aula.value.strip(), descripcion.value.strip(), id)

        if not success:
            page.snack_bar = ft.SnackBar(
                content=ft.Row(
                    [ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.WHITE),
                     ft.Text(f"Error: {msg}", color=ft.Colors.WHITE)],
                    spacing=10,
                ),
                bgcolor="#B22222",
                duration=3000,
                open=True,
            )
            return
        show_success(page, "✅ Aula creada correctamente")
        cerrar_modal(e)
        page.update()

    # ================================
    # BOTONES MODAL
    # ================================
    btn_guardar = ft.Container(
        content=ft.Text("Crear Aula", color="#FFFFFF", size=16, weight=ft.FontWeight.BOLD),
        gradient=ft.LinearGradient(colors=[COLOR_ACCENT, "#145C70"]),
        width=160,
        height=45,
        border_radius=8,
        alignment=ft.alignment.center,
        ink=True,
        on_click=crear_aula_action,
    )

    btn_cancelar = ft.Container(
        content=ft.Text("Cancelar", color=COLOR_TEXT_SEC, size=16, weight=ft.FontWeight.W_500),
        border=ft.border.all(1, "#2C2C2C"),
        border_radius=8,
        width=130,
        height=45,
        alignment=ft.alignment.center,
        ink=True,
        on_click=cerrar_modal,
    )

    # ================================
    # FORMULARIO MODAL
    # ================================
    form_container = ft.Container(
        width=700,
        height=360,
        bgcolor="#0B1418",
        border_radius=12,
        border=ft.border.all(1, "#1E2C30"),
        padding=30,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.ADD_BOX_OUTLINED, color=COLOR_ACCENT),
                        ft.Text("CREAR AULA", color=COLOR_TEXT, size=22, weight=ft.FontWeight.BOLD),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Divider(height=10, color="#1F3A44"),
                nombre_aula,
                descripcion,
                ft.Row([btn_cancelar, btn_guardar], alignment=ft.MainAxisAlignment.END, spacing=10),
            ],
            spacing=12,
        ),
    )

    modal_container = ft.Container(
        bgcolor=ft.Colors.with_opacity(0.6, ft.Colors.BLACK),
        expand=True,
        alignment=ft.alignment.center,
        content=form_container,
        visible=False,
    )

    # ================================
    # BOTONES PRINCIPALES (centrados)
    # ================================
    def create_button(icon, text, on_click=None, width=340, height=210):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, size=70, color="#FFFFFF"),
                    ft.Text(text, size=24, color="#FFFFFF", weight=ft.FontWeight.W_500),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            gradient=ft.LinearGradient(colors=[COLOR_BG_CARD, "#0C252D"]),
            border=ft.border.all(1, "#1F3A44"),
            border_radius=18,
            width=width,
            height=height,
            alignment=ft.alignment.center,
            ink=True,
            on_click=on_click,
            shadow=ft.BoxShadow(spread_radius=0.5, blur_radius=12, color="#0D0D0D", offset=ft.Offset(0, 4)),
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
        )

    btn_crear_aula = create_button(ft.Icons.ADD, "Crear Aula", on_click=abrir_modal)
    btn_tus_aulas = create_button(ft.Icons.GROUP, "Tus Aulas", on_click=lambda e: page.go("/tus_aulas"))
    btn_herramientas = create_button(
        ft.Icons.SETTINGS,
        "Herramientas",
        on_click=lambda e: page.go("/herramientas"),
        height=440,
    )

    botones = ft.Row(
        [
            ft.Column([btn_crear_aula, btn_tus_aulas], spacing=20),
            btn_herramientas,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=40,
    )

    # ================================
    # LAYOUT PRINCIPAL
    # ================================
    header = ft.Row([ft.Container(expand=True), logout_container], alignment=ft.MainAxisAlignment.END)

    contenido = ft.Column(
        [header, lbl_bienvenida, ft.Text(f"ID Usuario: {id}", color=COLOR_TEXT_SEC), ft.Container(height=30), botones],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    return ft.Container(
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#0C1C24", "#0E2329", "#08171C"],
        ),
        content=ft.Stack([contenido, modal_container]),
        alignment=ft.alignment.center,
        expand=True,
    )
