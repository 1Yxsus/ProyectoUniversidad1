import flet as ft
from app.controllers.usuario_controller import authenticate_user
from app.components.to_home import BotonHome


def LoginView(page: ft.Page):
    page.title = "Inicio de Sesión"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = ft.Colors.BLACK
    page.scroll = ft.ScrollMode.AUTO

    # --- Inputs estilizados ---
    correo_input = ft.TextField(
        label="Correo institucional",
        hint_text="ejemplo@universidad.edu",
        width=380,
        height=55,
        border_radius=12,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.WHITE),
        border_color=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
        focused_border_color=ft.Colors.BLUE_400,
        label_style=ft.TextStyle(color=ft.Colors.GREY_400),
        hint_style=ft.TextStyle(color=ft.Colors.GREY_600),
        text_style=ft.TextStyle(color=ft.Colors.WHITE),
        prefix_icon=ft.Icons.EMAIL_OUTLINED,
    )

    contrasena_input = ft.TextField(
        label="Contraseña",
        hint_text="Ingrese su contraseña",
        width=380,
        height=55,
        border_radius=12,
        password=True,
        can_reveal_password=True,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.WHITE),
        border_color=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
        focused_border_color=ft.Colors.BLUE_400,
        label_style=ft.TextStyle(color=ft.Colors.GREY_400),
        hint_style=ft.TextStyle(color=ft.Colors.GREY_600),
        text_style=ft.TextStyle(color=ft.Colors.WHITE),
        prefix_icon=ft.Icons.LOCK_OUTLINE,
    )

    mensaje_error = ft.Text("", color=ft.Colors.RED_400, size=13)

    # --- Función de login ---
    def iniciar_sesion(e):
        usuario = correo_input.value
        contrasena = contrasena_input.value

        user = authenticate_user(usuario, contrasena)

        if not usuario or not contrasena:
            mensaje_error.value = "Por favor, complete todos los campos."
            page.update()
            return

        if user:
            page.session.set("user", user)
            mensaje_error.value = ""
            snack_bar = ft.SnackBar(ft.Text("Inicio de sesión exitoso ✅"))
            snack_bar.open = True
            page.update()
            page.go("/options")
        else:
            mensaje_error.value = "Usuario o contraseña incorrectos."
            page.update()

    # --- Botón principal ---
    btn_login = ft.ElevatedButton(
        text="Iniciar Sesión",
        width=380,
        height=55,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_500,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=14),
            elevation=6,
            padding=ft.padding.symmetric(horizontal=20, vertical=15),
        ),
        on_click=iniciar_sesion,
    )

    # --- Enlace registro ---
    link_registro = ft.TextButton(
        text="¿No tienes una cuenta? Registrarse",
        style=ft.ButtonStyle(color=ft.Colors.GREY_400),
        on_click=lambda e: page.go("/register"),
    )

    logo = ft.Image(
        src="assets/images/logo_main.png",
        width=180,
        height=180,
        fit=ft.ImageFit.CONTAIN,
    )

    # --- Contenedor principal del login ---
    contenido_login = ft.Container(
        width=450,
        padding=ft.padding.all(40),
        border_radius=25,
        bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.WHITE),
        shadow=ft.BoxShadow(blur_radius=25, color=ft.Colors.with_opacity(0.15, ft.Colors.WHITE)),
        content=ft.Column(
            [   
                logo,
                ft.Text(
                    "Bienvenido de nuevo 👋",
                    size=26,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Inicia sesión para continuar con tu organización académica.",
                    size=14,
                    color=ft.Colors.GREY_400,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=25),
                correo_input,
                contrasena_input,
                ft.Container(height=10),
                mensaje_error,
                ft.Container(height=15),
                btn_login,
                ft.Container(height=10),
                link_registro,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
        ),
    )

    # --- Fondo con degradado sutil ---
    fondo = ft.Container(
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[
                ft.Colors.BLACK,
                ft.Colors.with_opacity(0.95, ft.Colors.BLUE_GREY_900),
            ],
        ),
        content=ft.Column(
            [
                ft.Container(
                    alignment=ft.alignment.top_left,
                    padding=ft.padding.only(top=20, left=30),
                    content=BotonHome(on_click=lambda e: page.go("/")),
                ),
                ft.Container(
                    alignment=ft.alignment.center,
                    expand=True,
                    content=contenido_login,
                ),
            ],
            expand=True,
        ),
        expand=True,
    )

    return fondo
