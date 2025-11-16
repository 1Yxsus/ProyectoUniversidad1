import flet as ft
from app.controllers.usuario_controller import obtener_usuario_por_id, actualizar_usuario
from app.utils.show_succes import show_success
from typing import Optional, Callable
import threading

def PerfilUsuarioView(page: ft.Page, id_usuario: int, on_user_update: Optional[Callable[[dict], None]] = None):
    page.title = "Aula 365 | Perfil de Usuario"
    page.bgcolor = "#000000"
    page.scroll = ft.ScrollMode.AUTO

    COLOR_PRIMARY = "#00B8D4"
    COLOR_TEXT = "#FFFFFF"
    COLOR_SUBTEXT = "#CCCCCC"
    COLOR_DIVIDER = "#333333"
    COLOR_MODAL = "#121212"

    # ============================================================
    # DATOS DEL USUARIO
    # ============================================================
    usuario = obtener_usuario_por_id(id_usuario)

    # ============================================================
    # ========== 1) MODAL EDITAR NOMBRE/APELLIDO/CORREO ===========
    # ============================================================

    input_nombre = ft.TextField(label="Nombre", bgcolor="#1E1E1E", border_radius=10)
    input_apellido = ft.TextField(label="Apellido", bgcolor="#1E1E1E", border_radius=10)
    input_correo = ft.TextField(label="Correo", bgcolor="#1E1E1E", border_radius=10)
    input_pass_confirm = ft.TextField(
        label="Contraseña Actual",
        password=True,
        can_reveal_password=True,
        bgcolor="#1E1E1E",
        border_radius=10,
    )

    modal_tipo = None  # nombre / apellido / correo

    # overlay temporal para mensajes de éxito
    success_overlay = None


    def abrir_modal_editar(tipo):
        nonlocal modal_tipo
        modal_tipo = tipo

        # precargar valores actuales y mostrar campo correspondiente
        input_nombre.value = usuario.get("nombre", "")
        input_apellido.value = usuario.get("apellido", "")
        input_correo.value = usuario.get("correo", "")
        input_pass_confirm.value = ""
        input_nombre.visible = (tipo == "nombre")
        input_apellido.visible = (tipo == "apellido")
        input_correo.visible = (tipo == "correo")
        input_pass_confirm.visible = (tipo == "correo")

        modal_editar_datos.visible = True
        page.update()

    def cerrar_modal_editar(e=None):
        modal_editar_datos.visible = False
        page.update()

    def guardar_datos(e):
        nonlocal usuario, modal_tipo

        # Obtener valores actuales para enviar a la función de actualización
        nombre_new = usuario.get("nombre", "")
        apellido_new = usuario.get("apellido", "")
        correo_new = usuario.get("correo", "")
        contrasena_actual = usuario.get("contrasena", "")

        try:
            if modal_tipo == "nombre":
                nombre_new = input_nombre.value.strip()
                if not nombre_new:
                    page.snack_bar = ft.SnackBar(ft.Text("El nombre no puede estar vacío.", color="white"), bgcolor="red")
                    page.snack_bar.open = True
                    page.update()
                    return

            elif modal_tipo == "apellido":
                apellido_new = input_apellido.value.strip()
                if not apellido_new:
                    page.snack_bar = ft.SnackBar(ft.Text("El apellido no puede estar vacío.", color="white"), bgcolor="red")
                    page.snack_bar.open = True
                    page.update()
                    return

            elif modal_tipo == "correo":
                correo_new = input_correo.value.strip()
                # validar contraseña actual para cambiar correo
                if input_pass_confirm.value.strip() == "":
                    page.snack_bar = ft.SnackBar(ft.Text("Debe ingresar su contraseña actual.", color="white"), bgcolor="red")
                    page.snack_bar.open = True
                    page.update()
                    return
                if input_pass_confirm.value != contrasena_actual:
                    page.snack_bar = ft.SnackBar(ft.Text("Contraseña incorrecta.", color="white"), bgcolor="red")
                    page.snack_bar.open = True
                    page.update()
                    return

            # llamar al controlador para persistir (actualiza todos los campos en la fila)
            ok = actualizar_usuario(id_usuario, nombre_new, apellido_new, correo_new, contrasena_actual)
        except Exception as ex:
            print("ERROR actualizar_usuario:", ex)
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al actualizar: {ex}", color="white"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        if ok:
            # actualizar la variable local y la session si existe
            usuario["nombre"] = nombre_new
            usuario["apellido"] = apellido_new
            usuario["correo"] = correo_new
            try:
                sess_user = page.session.get("user") or {}
                if sess_user:
                    sess_user.update({"nombre": usuario["nombre"], "apellido": usuario["apellido"], "correo": usuario["correo"]})
                    page.session.set("user", sess_user)
            except Exception:
                pass
            
            # actualizar los controles de la interfaz para que reflejen los cambios
            name_text.value = usuario["nombre"]
            apellido_text.value = usuario["apellido"]
            correo_text.value = usuario["correo"]

            # Notificar al caller (ej. dashboard) para que actualice la sidebar
            try:
                if on_user_update:
                    # enviar el diccionario actualizado (puedes adaptar la forma)
                    updated_user = {
                        "id_usuario": usuario.get("id_usuario"),
                        "nombre": usuario["nombre"],
                        "apellido": usuario["apellido"],
                        "correo": usuario["correo"],
                    }
                    on_user_update(updated_user)
            except Exception:
                pass


            # mostrar confirmación visual y opcional snack
            show_success(page,"Datos guardados ✔")
            page.snack_bar = ft.SnackBar(ft.Text("Datos actualizados correctamente.", color="white"), bgcolor=COLOR_PRIMARY)
            page.snack_bar.open = True


            cerrar_modal_editar()
            page.snack_bar = ft.SnackBar(ft.Text("Datos actualizados correctamente.", color="white"), bgcolor=COLOR_PRIMARY)
            page.snack_bar.open = True
            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("No se pudo actualizar los datos.", color="white"), bgcolor="red")
            page.snack_bar.open = True
            page.update()

    modal_editar_datos = ft.Container(
        visible=False,
        expand=True,
        bgcolor=ft.Colors.with_opacity(0.7, "#000000"),
        alignment=ft.alignment.center,
        content=ft.Container(
            width=500,
            height=300,
            padding=30,
            bgcolor=COLOR_MODAL,
            border_radius=12,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("Editar Datos", size=22, weight=ft.FontWeight.BOLD, color=COLOR_TEXT),
                            ft.Container(expand=True),
                            ft.IconButton(icon=ft.Icons.CLOSE, icon_color="white", on_click=cerrar_modal_editar),
                        ]
                    ),
                    input_nombre,
                    input_apellido,
                    input_correo,
                    input_pass_confirm,
                    ft.Row(
                        [
                            ft.TextButton("Cancelar", on_click=cerrar_modal_editar),
                            ft.ElevatedButton("Guardar", bgcolor=COLOR_PRIMARY, color="white", on_click=guardar_datos),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                spacing=15,
            )
        )
    )

    # ============================================================
    # ======================== 2) MODAL CONTRASEÑA ================
    # ============================================================

    input_old_pass = ft.TextField(
        label="Contraseña Actual",
        password=True,
        can_reveal_password=True,
        bgcolor="#1E1E1E",
        border_radius=10,
    )
    input_new_pass = ft.TextField(
        label="Nueva Contraseña",
        password=True,
        can_reveal_password=True,
        bgcolor="#1E1E1E",
        border_radius=10,
    )
    input_repeat_pass = ft.TextField(
        label="Repetir Contraseña",
        password=True,
        can_reveal_password=True,
        bgcolor="#1E1E1E",
        border_radius=10,
    )

    def abrir_modal_contrasena(e=None):
        input_old_pass.value = ""
        input_new_pass.value = ""
        input_repeat_pass.value = ""
        modal_contrasena.visible = True
        page.update()

    def cerrar_modal_contrasena(e=None):
        modal_contrasena.visible = False
        page.update()

    def guardar_contrasena(e):
        # validar coincidencia
        if input_new_pass.value != input_repeat_pass.value:
            page.snack_bar = ft.SnackBar(ft.Text("Las contraseñas no coinciden.", color="white"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        # validar contraseña actual
        contrasena_actual = usuario.get("contrasena", "")
        if input_old_pass.value != contrasena_actual:
            page.snack_bar = ft.SnackBar(ft.Text("Contraseña actual incorrecta.", color="white"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        if input_new_pass.value.strip() == "":
            page.snack_bar = ft.SnackBar(ft.Text("La nueva contraseña no puede estar vacía.", color="white"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        # persistir el cambio
        try:
            ok = actualizar_usuario(id_usuario, usuario.get("nombre", ""), usuario.get("apellido", ""), usuario.get("correo", ""), input_new_pass.value)
        except Exception as ex:
            print("ERROR actualizar_contrasena:", ex)
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al cambiar la contraseña: {ex}", color="white"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        if ok:
            usuario["contrasena"] = input_new_pass.value
            try:
                sess_user = page.session.get("user") or {}
                if sess_user:
                    sess_user["contrasena"] = usuario["contrasena"]
                    page.session.set("user", sess_user)
            except Exception:
                pass
            # mostrar confirmación visual y snack
            show_success(page,"Contraseña actualizada ✔")
            cerrar_modal_contrasena()
            page.snack_bar = ft.SnackBar(ft.Text("Contraseña actualizada con éxito.", color="white"), bgcolor=COLOR_PRIMARY)
            page.snack_bar.open = True
            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("No se pudo actualizar la contraseña.", color="white"), bgcolor="red")
            page.snack_bar.open = True
            page.update()

    modal_contrasena = ft.Container(
        visible=False,
        expand=True,
        bgcolor=ft.Colors.with_opacity(0.7, "#000000"),
        alignment=ft.alignment.center,
        content=ft.Container(
            width=500,
            height=400,
            padding=30,
            bgcolor=COLOR_MODAL,
            border_radius=12,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("Cambiar Contraseña", size=22, weight=ft.FontWeight.BOLD, color=COLOR_TEXT),
                            ft.Container(expand=True),
                            ft.IconButton(icon=ft.Icons.CLOSE, icon_color="white", on_click=cerrar_modal_contrasena),
                        ]
                    ),
                    input_old_pass,
                    input_new_pass,
                    input_repeat_pass,
                    ft.Row(
                        [
                            ft.TextButton("Cancelar", on_click=cerrar_modal_contrasena),
                            ft.ElevatedButton("Guardar", bgcolor=COLOR_PRIMARY, color="white", on_click=guardar_contrasena),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                spacing=15,
            )
        )
    )

    # ============================================================
    # IMPORTANTE: Agregar modales SOLO en overlay
    # ============================================================
    # IMPORTANTE: Agregar modales SOLO en overlay (usar append en vez de asignar)
    if modal_editar_datos not in page.overlay:
        page.overlay.append(modal_editar_datos)
    if modal_contrasena not in page.overlay:
        page.overlay.append(modal_contrasena)
    # opcional: forzar render inicial
    page.update()

    # Controles dinámicos que muestran los datos actuales (se actualizan tras guardar)
    name_text = ft.Text(usuario.get("nombre", ""), color=COLOR_SUBTEXT, size=16)
    apellido_text = ft.Text(usuario.get("apellido", ""), color=COLOR_SUBTEXT, size=16)
    correo_text = ft.Text(usuario.get("correo", ""), color=COLOR_SUBTEXT, size=16)


    # ============================================================
    # ELEMENTO CAMPO
    # ============================================================
    def campo(label, text_control: ft.Text, tipo):
        return ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(label, size=18, weight=ft.FontWeight.BOLD, color=COLOR_TEXT),
                        ft.Container(expand=True),
                        ft.ElevatedButton(
                            "Editar",
                            bgcolor=COLOR_PRIMARY,
                            color="white",
                            height=35,
                            width=80,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                            on_click=lambda e: abrir_modal_editar(tipo),
                        )
                    ]
                ),
                text_control,
                ft.Divider(height=20, thickness=1, color=COLOR_DIVIDER),
            ]
        )
    # ============================================================
    # HEADER
    # ============================================================
    header = ft.Row(
        [
            ft.Text("Perfil de Usuario", size=42, weight=ft.FontWeight.BOLD, color=COLOR_TEXT),
            ft.Container(expand=True),
            ft.IconButton(
                icon=ft.Icons.HOME,
                icon_color="white",
                icon_size=28,
                style=ft.ButtonStyle(shape=ft.CircleBorder(), bgcolor="#222"),
                on_click=lambda e: page.go("/options"),
            )
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # ============================================================
    # LAYOUT FINAL (SIN MODALES ADENTRO)
    # ============================================================
    return ft.Container(
        content=ft.Column(
            [
                header,
                ft.Container(height=30),
                campo("Nombre", name_text, "nombre"),
                campo("Apellido", apellido_text, "apellido"),
                campo("Correo", correo_text, "correo"),
                ft.Container(height=40),
                ft.Text("Contraseña y Autenticación", size=20, weight=ft.FontWeight.BOLD, color=COLOR_TEXT),
                ft.ElevatedButton("Cambiar Contraseña", bgcolor=COLOR_PRIMARY, color="white", on_click=abrir_modal_contrasena),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=40,
        expand=True,
    )
