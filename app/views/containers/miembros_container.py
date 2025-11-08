import flet as ft
from app.controllers.aulas_usuario_controller import obtener_miembros_de_aula, eliminar_usuario_de_aula

def MiembrosAulaView(page: ft.Page, id_aula: int, miembros_list=None):
    """
    Vista moderna para mostrar los miembros de un aula.
    """

    # --- CONFIGURACIÓN DE PÁGINA ---
    page.title = "Aula 365 | Miembros del Aula"
    page.bgcolor = "#000000"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    # --- TÍTULO PRINCIPAL ---
    titulo = ft.Text(
        "Miembros del Aula",
        size=40,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE,
    )

    # --- BOTÓN HOME ---
    btn_home = ft.IconButton(
        icon=ft.Icons.HOME,
        icon_color=ft.Colors.WHITE,
        icon_size=30,
        style=ft.ButtonStyle(
            shape=ft.CircleBorder(),
            bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
        ),
        tooltip="Volver al inicio",
        on_click=lambda e: page.go("/options"),
    )

    miembros_list = obtener_miembros_de_aula(id_aula)

    # --- LISTA DE MIEMBROS ---
    if not miembros_list:
        # datos de prueba si no se pasa lista
        miembros_list = [f"Apellido Nombre {i+1}" for i in range(8)]


    def eliminar_y_refrescar(e, miembro):
        try:
            eliminar_usuario_de_aula(id_aula, miembro.get("id_usuario"))
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al eliminar: {ex}"))
            page.snack_bar.open = True
            page.update()
            return

        # recargar lista desde la BD
        nuevos_miembros = obtener_miembros_de_aula(id_aula)

        # actualizar el contenido del contenedor (lista_miembros se define más abajo pero existe en el cierre)
        try:
            lista_miembros.content.controls = [card_miembro(m) for m in nuevos_miembros]
        except NameError:
            # si aún no existe lista_miembros, actualizar la variable local para cuando se cree
            pass

        page.snack_bar = ft.SnackBar(ft.Text(f"🗑️ {miembro.get('nombre')} eliminado"))
        page.snack_bar.open = True
        page.update()

    # --- FUNCION PARA CREAR TARJETA DE MIEMBRO ---
    def card_miembro(miembro):
        nombre_completo = f"{miembro.get('nombre','').strip()} {miembro.get('apellido','').strip()}".strip()
        email = miembro.get("email", "")
        return ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(nombre_completo, size=16, color=ft.Colors.WHITE, weight=ft.FontWeight.W_400),
                            ft.Text(email, size=12, color=ft.Colors.GREY),
                        ],
                        tight=True,
                    ),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color=ft.Colors.RED,
                        tooltip="Eliminar miembro",
                        on_click=lambda e, m=miembro: eliminar_y_refrescar(e, m)
                        ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor="#2B2B2B",
            border_radius=10,
            padding=ft.padding.symmetric(horizontal=20, vertical=12),
            border=ft.border.all(1, "#333333"),
            width=500,
        )

    # --- CONTENEDOR CON SCROLL ---
    lista_miembros = ft.Container(
        expand=True,
        content=ft.Column(
            [card_miembro(m) for m in miembros_list],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        ),
    )

    # --- ESTRUCTURA PRINCIPAL ---
    contenido = ft.Column(
        [
            ft.Row([titulo, ft.Container(expand=True), btn_home], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(height=30),
            lista_miembros,
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        expand=True,
    )

    # --- CONTAINER FINAL ---
    layout = ft.Container(
        expand=True,
        padding=ft.padding.all(50),
        content=contenido,
        alignment=ft.alignment.top_left,
    )

    return layout
