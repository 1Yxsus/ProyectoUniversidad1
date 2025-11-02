import flet as ft
from app.controllers.auth_controller import register_user
from app.components.to_home import BotonHome
from app.utils.database import get_connection
import mysql.connector

def RegisterView(page: ft.Page):

    page.title = "Registro de Usuario"
    page.bgcolor = ft.Colors.BLACK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    apellido_input = ft.TextField(label="Apellidos", width=350, height=50,
                                  border_radius=10, color=ft.Colors.BLACK,
                                  bgcolor=ft.Colors.WHITE,
                                  label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY))

    nombre_input = ft.TextField(label="Nombre", width=350, height=50,
                                border_radius=10, color=ft.Colors.BLACK,
                                bgcolor=ft.Colors.WHITE,
                                label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY))

    correo_input = ft.TextField(label="Correo institucional", width=350, height=50,
                                border_radius=10, color=ft.Colors.BLACK,
                                bgcolor=ft.Colors.WHITE,
                                label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY))

    contrasena_input = ft.TextField(label="Contraseña", width=350, height=50,
                                    border_radius=10, password=True,
                                    can_reveal_password=True,
                                    color=ft.Colors.BLACK,
                                    bgcolor=ft.Colors.WHITE,
                                    label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY))

    confirmar_input = ft.TextField(label="Confirmar contraseña", width=350, height=50,
                                   border_radius=10, password=True,
                                   can_reveal_password=True,
                                   color=ft.Colors.BLACK,
                                   bgcolor=ft.Colors.WHITE,
                                   label_style=ft.TextStyle(color=ft.Colors.BLUE_GREY))

    mensaje_error = ft.Text("", color=ft.Colors.RED_400, size=13)

    # def registrar_usuario(e):
    #     apellido = apellido_input.value.strip() if apellido_input.value else ""
    #     nombre = nombre_input.value.strip() if nombre_input.value else ""
    #     correo = correo_input.value.strip() if correo_input.value else ""
    #     contrasena = contrasena_input.value.strip() if contrasena_input.value else ""
    #     confirmar = confirmar_input.value.strip() if confirmar_input.value else ""

    #     if not apellido or not nombre or not correo or not contrasena or not confirmar:
    #         mensaje_error.value = "Por favor, complete todos los campos."
    #         page.update()
    #         return

    #     if contrasena != confirmar:
    #         mensaje_error.value = "Las contraseñas no coinciden."
    #         page.update()
    #         return

    #     try:
    #         db = get_connection()
    #         cursor = db.cursor()

    #         cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
    #         if cursor.fetchone():
    #             mensaje_error.value = "⚠ El correo ya está registrado"
    #             page.update()
    #             cursor.close()
    #             db.close()
    #             return

    #         cursor.execute("""
    #             INSERT INTO usuario (nombre, apellido, correo, contraseña)
    #             VALUES (%s, %s, %s, %s)
    #         """, (nombre, apellido, correo, contrasena))
    #         db.commit()
    #         cursor.close()
    #         db.close()

    #         snack_bar = ft.SnackBar(
    #             content=ft.Text("Registro exitoso ✅"),
    #             bgcolor=ft.Colors.GREEN_700
    #         )
    #         page.overlay.append(snack_bar)
    #         snack_bar.open = True
    #         page.update()
    #         page.go("/login")

    #     except Exception as ex:
    #         mensaje_error.value = f"Error al registrar: {str(ex)}"
    #         page.update()

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

        # Llamada al controlador que centraliza la lógica de BD
        success, msg = register_user(nombre, apellido, correo, contrasena)
        if not success:
            mensaje_error.value = f"⚠ {msg}"
            page.update()
            return

        # éxito
        snack_bar = ft.SnackBar(
            content=ft.Text("Registro exitoso ✅"),
            bgcolor=ft.Colors.GREEN_700
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
        page.go("/login")

    btn_registrar = ft.ElevatedButton(
        text="Registrarse",
        width=350,
        height=50,
        bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
        color=ft.Colors.WHITE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            bgcolor=ft.Colors.GREY_900,
        ),
        on_click=registrar_usuario,
    )

    link_login = ft.TextButton(
        text="Volver al inicio de sesión",
        style=ft.ButtonStyle(color=ft.Colors.GREY_400),
        on_click=lambda e: page.go("/login"),
    )

    contenido_register = ft.Column(
        [
            ft.Text("Registro de Usuario", size=20,
                    weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Container(height=20),
            apellido_input, nombre_input, correo_input,
            contrasena_input, confirmar_input,
            ft.Container(height=10),
            mensaje_error, btn_registrar, link_login,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
    )

    contenido = ft.Column(
        [
            BotonHome(on_click=lambda e: page.go("/")),
            ft.Container(height=20),
            contenido_register,
        ],
        spacing=10,
    )

    return ft.Container(
        content=contenido,
        alignment=ft.alignment.center,
        expand=True,
        bgcolor=ft.Colors.BLACK,
    )
