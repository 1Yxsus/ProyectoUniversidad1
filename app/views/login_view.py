import flet as ft
from app.controllers.usuario_controller import authenticate_user
from app.components.to_home import BotonHome

def LoginView(page: ft.Page):

    page.title = "Inicio de Sesión"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = ft.Colors.BLACK

    correo_input = ft.TextField(
        label="Correo",
        hint_text="Ingrese su correo institucional",
        width=350,
        height=50,
        border_radius=10,
        color=ft.Colors.BLACK,
        bgcolor=ft.Colors.WHITE,
        label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY)         # opcional: color de la etiqueta
    )

    contrasena_input = ft.TextField(
        label="Contraseña",
        hint_text="Ingrese su contraseña",
        width=350,
        height=50,
        border_radius=10,
        password=True,
        can_reveal_password=True,
        color=ft.Colors.BLACK,
        bgcolor=ft.Colors.WHITE,
        label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY)
    )

    mensaje_error = ft.Text("", color=ft.Colors.RED_400, size=13)

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

    btn_login = ft.ElevatedButton(
        text="Iniciar Sesión",
        width=350,
        height=50,
        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
        color=ft.Colors.WHITE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            bgcolor=ft.Colors.GREY_900,
        ),
        on_click=iniciar_sesion,
    )

    link_registro = ft.TextButton(
        text="Registrarse",
        style=ft.ButtonStyle(color=ft.Colors.GREY_400),
        on_click=lambda e: page.go("/register"),
    )

    contenido_login = ft.Column(
        [   
            ft.Text("Name", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Container(height=30),
            correo_input,
            contrasena_input,
            ft.Container(height=10),
            mensaje_error,
            btn_login,
            link_registro,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
    )


    contenido = ft.Column(
        [
            BotonHome(on_click=lambda e: page.go("/")),
            ft.Container(height=20),
            contenido_login
        ],
        spacing=10,
        expand=True
    )

    return ft.Container(
        content=contenido,
        alignment=ft.alignment.center,  # 👈 centra vertical y horizontal
        expand=True,                    # ocupa toda la pantalla
        bgcolor=ft.Colors.BLACK
    )
