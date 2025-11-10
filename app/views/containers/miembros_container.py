import flet as ft
from app.controllers.aulas_usuario_controller import (
    obtener_miembros_de_aula,
    eliminar_usuario_de_aula,
    asignar_admin_a_usuario,
    agregar_usuario_a_aula,
)
from app.utils.is_staff_verification import is_staff_verification
from app.utils.vald_text_fields import validar_formulario


def MiembrosAulaView(page: ft.Page, func_load_content, id_aula: int, miembros_list=None):
    """
    Vista coherente con el estilo dark petróleo del dashboard.
    """

    # ------------------------------------------------------
    # CONFIGURACIÓN GENERAL
    # ------------------------------------------------------
    page.title = "UniRed | Miembros del Aula"
    page.scroll = ft.ScrollMode.AUTO

    # Paleta unificada
    COLOR_BG_CARD = "#0E1E25"
    COLOR_BG_CARD_HOVER = "#152B33"
    COLOR_BORDER_CARD = "#1F3A44"
    COLOR_ACCENT = "#1C8DB0"
    COLOR_TEXT_PRIMARY = "#EAEAEA"
    COLOR_TEXT_SECONDARY = "#AAB6B8"

    # ------------------------------------------------------
    # DATOS DE USUARIO Y AULA
    # ------------------------------------------------------
    is_staff = is_staff_verification(page, id_aula)
    current_user = page.session.get("user") or {}
    current_user_id = current_user.get("id_usuario")
    miembros_list = obtener_miembros_de_aula(id_aula)

    # ------------------------------------------------------
    # CABECERA
    # ------------------------------------------------------
    titulo = ft.Text(
        "Miembros del Aula",
        size=36,
        weight=ft.FontWeight.BOLD,
        color=COLOR_TEXT_PRIMARY,
    )

    btn_volver = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_color="#EAEAEA",
        icon_size=26,
        style=ft.ButtonStyle(
            shape=ft.CircleBorder(),
            bgcolor=ft.Colors.with_opacity(0.1, COLOR_ACCENT),
        ),
        tooltip="Volver",
        on_click=lambda e: func_load_content("Editar Aula"),
    )

    btn_home = ft.IconButton(
        icon=ft.Icons.HOME,
        icon_color="#EAEAEA",
        icon_size=26,
        style=ft.ButtonStyle(
            shape=ft.CircleBorder(),
            bgcolor=ft.Colors.with_opacity(0.1, COLOR_ACCENT),
        ),
        tooltip="Volver al inicio",
        on_click=lambda e: page.go("/options"),
    )

    btn_add_member = ft.Container(
        content=ft.Row(
            [ft.Icon(ft.Icons.ADD, color="#FFFFFF"), ft.Text("Añadir Miembro", color="#FFFFFF")],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=6,
        ),
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=[COLOR_ACCENT, "#186678"],
        ),
        width=200,
        height=45,
        border_radius=8,
        ink=True,
        visible=is_staff,
        on_click=lambda e: abrir_modal(e),
    )

    header = ft.Row(
        [titulo, ft.Container(expand=True), ft.Row([btn_add_member, btn_volver, btn_home])],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # ------------------------------------------------------
    # MODAL PARA AGREGAR MIEMBRO
    # ------------------------------------------------------
    id_usuario = ft.TextField(
        label="ID del usuario a agregar",
        bgcolor="#0D1A20",
        border_radius=8,
        border_color="#1F3A44",
        focused_border_color=COLOR_ACCENT,
        color=COLOR_TEXT_PRIMARY,
        width=300,
    )

    modal_title = ft.Text("Agregar Miembro", weight=ft.FontWeight.BOLD, size=22, color=COLOR_TEXT_PRIMARY)
    campos = [id_usuario]

    def validar_y_agregar(e):
        if not validar_formulario(page, campos):
            return
        try:
            agregar_usuario_a_aula(id_aula, id_usuario.value, rol="ALUMNO")
            cerrar_modal(e)
            reload_members()
            page.snack_bar = ft.SnackBar(ft.Text("✅ Miembro agregado correctamente"))
            page.snack_bar.open = True
            page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), bgcolor="#A93226")
            page.snack_bar.open = True
            page.update()

    btn_guardar = ft.Container(
        content=ft.Text("Invitar", color="#FFFFFF", size=16, weight=ft.FontWeight.W_500),
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=[COLOR_ACCENT, "#145C70"],
        ),
        width=150,
        height=45,
        border_radius=8,
        alignment=ft.alignment.center,
        ink=True,
        on_click=validar_y_agregar,
    )

    btn_cancelar = ft.Container(
        content=ft.Text("Cancelar", color=COLOR_TEXT_SECONDARY, size=16),
        width=120,
        height=45,
        border_radius=8,
        alignment=ft.alignment.center,
        ink=True,
        border=ft.border.all(1, "#2C2C2C"),
        on_click=lambda e: cerrar_modal(e),
    )

    form_container = ft.Container(
        width=500,
        height=250,
        bgcolor="#0B1418",
        border_radius=12,
        padding=30,
        border=ft.border.all(1, "#1E2C30"),
        content=ft.Column(
            [
                ft.Row([ft.Icon(ft.Icons.ADD_BOX_OUTLINED, color=COLOR_ACCENT), modal_title], spacing=10),
                ft.Divider(height=10, color="transparent"),
                id_usuario,
                ft.Container(height=15),
                ft.Row([btn_cancelar, btn_guardar], alignment=ft.MainAxisAlignment.END, spacing=10),
            ],
            spacing=12,
        ),
    )

    modal_container = ft.Container(
        bgcolor=ft.Colors.with_opacity(0.65, "#000000"),
        expand=True,
        alignment=ft.alignment.center,
        content=form_container,
        visible=False,
    )

    def abrir_modal(e):
        modal_container.visible = True
        page.update()

    def cerrar_modal(e):
        modal_container.visible = False
        page.update()

    # ------------------------------------------------------
    # TARJETAS DE MIEMBROS
    # ------------------------------------------------------
    def open_confirm_assign(e, miembro):
        nombre = f"{miembro.get('nombre','')} {miembro.get('apellido','')}".strip()

        def _on_confirm(ev):
            try:
                asignar_admin_a_usuario(id_aula, miembro.get("id_usuario"))
                reload_members()
                page.snack_bar = ft.SnackBar(ft.Text("✅ Administrador asignado"))
                page.snack_bar.open = True
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"))
                page.snack_bar.open = True
            cerrar_modal(ev)

        confirm_container = ft.Container(
            width=500,
            height=160,
            bgcolor="#0B1418",
            border_radius=12,
            border=ft.border.all(1, "#1E2C30"),
            padding=20,
            content=ft.Column(
                [
                    ft.Text("Confirmar asignación", size=18, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_PRIMARY),
                    ft.Text(f"¿Asignar rol ADMIN a {nombre}?", color=COLOR_TEXT_SECONDARY),
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Text("Cancelar", color="#AAAAAA"),
                                border=ft.border.all(1, "#2C2C2C"),
                                border_radius=8,
                                padding=ft.padding.symmetric(horizontal=16, vertical=8),
                                on_click=cerrar_modal,
                                ink=True,
                            ),
                            ft.Container(
                                content=ft.Text("Confirmar", color="#FFFFFF"),
                                gradient=ft.LinearGradient(
                                    begin=ft.alignment.center_left,
                                    end=ft.alignment.center_right,
                                    colors=[COLOR_ACCENT, "#145C70"],
                                ),
                                border_radius=8,
                                padding=ft.padding.symmetric(horizontal=16, vertical=8),
                                ink=True,
                                on_click=_on_confirm,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
                spacing=12,
            ),
        )

        modal_container.content = confirm_container
        modal_container.visible = True
        page.update()

    def eliminar_y_refrescar(e, miembro):
        try:
            eliminar_usuario_de_aula(id_aula, miembro.get("id_usuario"))
            reload_members()
            page.snack_bar = ft.SnackBar(ft.Text("🗑 Miembro eliminado"))
            page.snack_bar.open = True
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al eliminar: {ex}"))
            page.snack_bar.open = True
        page.update()

    def card_miembro(miembro):
        nombre_completo = f"{miembro.get('nombre','')} {miembro.get('apellido','')}".strip()
        email = miembro.get("email", "")
        is_admin = str(miembro.get("rol","")).upper() == "ADMIN"

        acciones = []
        if is_staff and not is_admin:
            acciones.append(
                ft.IconButton(
                    icon=ft.Icons.STAR_BORDER,
                    icon_color=COLOR_ACCENT,
                    tooltip="Asignar como ADMIN",
                    on_click=lambda e, m=miembro: open_confirm_assign(e, m),
                )
            )
        if is_staff:
            acciones.append(
                ft.IconButton(
                    icon=ft.Icons.DELETE,
                    icon_color="#D9534F",
                    tooltip="Eliminar miembro",
                    on_click=lambda e, m=miembro: eliminar_y_refrescar(e, m),
                )
            )

        badge = ft.Container(
            content=ft.Text("ADMIN", size=10, color="#FFFFFF"),
            padding=ft.padding.symmetric(horizontal=8, vertical=4),
            bgcolor="#1C8DB0",
            border_radius=6,
            visible=is_admin,
        )

        return ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Row([ft.Text(nombre_completo, size=16, color=COLOR_TEXT_PRIMARY, weight=ft.FontWeight.W_600), badge], spacing=8),
                            ft.Text(email, size=12, color=COLOR_TEXT_SECONDARY),
                        ]
                    ),
                    ft.Container(expand=True),
                    ft.Row(acciones, spacing=5),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLOR_BG_CARD, "#0C252D"],
            ),
            border_radius=10,
            border=ft.border.all(1, COLOR_BORDER_CARD),
            padding=ft.padding.symmetric(horizontal=20, vertical=12),
            on_hover=lambda e: (
                setattr(
                    e.control,
                    "bgcolor",
                    ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=[COLOR_BG_CARD_HOVER, "#133540"]
                    ) if e.data == "true" else
                    ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=[COLOR_BG_CARD, "#0C252D"]
                    ),
                ),
                e.control.update(),
            ),
        )

    # ------------------------------------------------------
    # LISTA DE MIEMBROS
    # ------------------------------------------------------
    def reload_members():
        nonlocal miembros_list
        miembros_list = obtener_miembros_de_aula(id_aula)
        lista_miembros.content.controls = [card_miembro(m) for m in miembros_list]
        page.update()

    lista_miembros = ft.Container(
        expand=True,
        content=ft.Column([card_miembro(m) for m in miembros_list], spacing=15, scroll=ft.ScrollMode.AUTO),
    )

    # ------------------------------------------------------
    # ESTRUCTURA PRINCIPAL
    # ------------------------------------------------------
    contenido = ft.Column(
        [header, ft.Container(height=25), lista_miembros],
        spacing=20,
        expand=True,
    )

    layout = ft.Container(
        padding=ft.padding.all(50),
        content=contenido,
        expand=True,
    )

    return ft.Stack(
        [
            ft.Container(
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=["#0C1C24", "#0E2329", "#08171C"],
                ),
                expand=True,
            ),
            layout,
            modal_container,
        ],
        expand=True,
    )
