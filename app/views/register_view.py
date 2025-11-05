import flet as ft
from app.controllers.usuario_controller import register_user
from app.components.to_home import BotonHome


def RegisterView(page: ft.Page):
    page.title = "Registro de Usuario"
    page.bgcolor = ft.Colors.BLACK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    # --- Inputs con estilo moderno ---
    apellido_input = ft.TextField(
        label="Apellidos",
        hint_text="Ingrese sus apellidos",
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
        prefix_icon=ft.Icons.BADGE_OUTLINED,
    )

    nombre_input = ft.TextField(
        label="Nombres",
        hint_text="Ingrese sus nombres",
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
        prefix_icon=ft.Icons.PERSON_OUTLINE,
    )

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
        hint_text="Crea una contraseña",
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

    confirmar_input = ft.TextField(
        label="Confirmar contraseña",
        hint_text="Repita su contraseña",
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

    # --- Función de registro ---
    def registrar_usuario(e):
        apellido = apellido_input.value.strip() if apellido_input.value else ""
        nombre = nombre_input.value.strip() if nombre_input.value else ""
        correo = correo_input.value.strip() if correo_input.value else ""
        contrasena = contrasena_input.value.strip() if contrasena_input.value else ""
        confirmar = confirmar_input.value.strip() if confirmar_input.value else ""

        if not apellido or not nombre or not correo or not contrasena or not confirmar:
            mensaje_error.value = "Por favor, complete todos los campos."
            page.update()
            return

        if contrasena != confirmar:
            mensaje_error.value = "Las contraseñas no coinciden."
            page.update()
            return

        success, msg = register_user(nombre, apellido, correo, contrasena)
        if not success:
            mensaje_error.value = f"⚠ {msg}"
            page.update()
            return

        snack_bar = ft.SnackBar(
            content=ft.Text("Registro exitoso ✅"),
            bgcolor=ft.Colors.GREEN_700,
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
        page.go("/login")

    # --- Botón de acción ---
    btn_registrar = ft.ElevatedButton(
        text="Registrarse",
        width=380,
        height=55,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_500,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=14),
            elevation=6,
            padding=ft.padding.symmetric(horizontal=20, vertical=15),
        ),
        on_click=registrar_usuario,
    )

    # --- Enlace para volver al login ---
    link_login = ft.TextButton(
        text="¿Ya tienes una cuenta? Inicia sesión",
        style=ft.ButtonStyle(color=ft.Colors.GREY_400),
        on_click=lambda e: page.go("/login"),
    )

    # --- Contenedor principal del formulario ---
    contenido_register = ft.Container(
        width=460,
        padding=ft.padding.all(40),
        border_radius=25,
        bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.WHITE),
        shadow=ft.BoxShadow(blur_radius=25, color=ft.Colors.with_opacity(0.15, ft.Colors.WHITE)),
        content=ft.Column(
            [
                ft.Text(
                    "Crea tu cuenta ✨",
                    size=26,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Únete a UniRed y mejora tu organización académica.",
                    size=14,
                    color=ft.Colors.GREY_400,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=25),
                apellido_input,
                nombre_input,
                correo_input,
                contrasena_input,
                confirmar_input,
                ft.Container(height=10),
                mensaje_error,
                ft.Container(height=15),
                btn_registrar,
                ft.Container(height=10),
                link_login,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
        ),
    )

    # --- Fondo con degradado y botón Home ---
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
                    content=contenido_register,
                ),
            ],
            expand=True,
        ),
        expand=True,
    )

    return fondo
