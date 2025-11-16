import flet as ft
from app.controllers.aulas_usuario_controller import (
    obtener_miembros_de_aula,
    eliminar_usuario_de_aula,
    asignar_admin_a_usuario,
    agregar_usuario_a_aula,
)
from app.utils.is_staff_verification import is_staff_verification
from app.utils.vald_text_fields import validar_formulario
from app.utils.show_succes import show_success


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
    # ------------------------------------------------------
    # TABLA DE MIEMBROS (NUEVO)
    # ------------------------------------------------------

    def asignar_admin_accion(miembro):
        """Crea un modal independiente en overlay para confirmar asignación de admin."""
        # modal content
        title = ft.Text("Confirmar asignación de Admin", weight=ft.FontWeight.BOLD)
        body = ft.Text(f"¿Asignar rol ADMIN a {miembro.get('apellido','')} {miembro.get('nombre','')} (ID {miembro.get('id_usuario')})?")

        def cerrar(e=None):
            try:
                page.overlay.remove(modal)
            except Exception:
                pass
            page.update()

        def confirmar(e):
            try:
                asignar_admin_a_usuario(id_aula, miembro["id_usuario"])
                reload_members()
                show_success(page, "🔑 Rol ADMIN asignado correctamente")
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), bgcolor="#A93226")
                page.snack_bar.open = True
            finally:
                cerrar()

        actions = ft.Row(
            [
                ft.TextButton("Cancelar", on_click=lambda e: cerrar()),
                ft.ElevatedButton("Confirmar", on_click=confirmar),
            ],
            alignment=ft.MainAxisAlignment.END,
            spacing=12,
        )

        modal = ft.Container(
            bgcolor=ft.Colors.with_opacity(0.65, "#000000"),
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Container(
                width=520,
                height=190,
                padding=ft.padding.all(20),
                border_radius=10,
                bgcolor="#0B1418",
                content=ft.Column([ft.Row([title]), ft.Divider(height=8), body, ft.Container(height=12), actions], spacing=12),
            ),
        )

        page.overlay.append(modal)
        page.update()

    def eliminar_miembro_accion(miembro):
        """Crea un modal independiente en overlay para confirmar eliminación."""
        title = ft.Text("Confirmar eliminación", weight=ft.FontWeight.BOLD)
        body = ft.Text(f"¿Eliminar a {miembro.get('apellido','')} {miembro.get('nombre','')} (ID {miembro.get('id_usuario')}) del aula? Esta acción no se puede deshacer.")

        def cerrar(e=None):
            try:
                page.overlay.remove(modal)
            except Exception:
                pass
            page.update()

        def confirmar(e):
            try:
                eliminar_usuario_de_aula(id_aula, miembro["id_usuario"])
                # Si el usuario se eliminó a sí mismo, navegamos al listado de aulas
                is_self = miembro.get("id_usuario") == current_user_id
                if is_self:
                    # cerrar modal y llevar al apartado "Aulas"
                    try:
                        page.overlay.remove(modal)
                    except Exception:
                        pass
                    page.update()
                    try:
                        page.go("/tus_aulas")
                    except Exception:
                        func_load_content("Aulas")
                    return
                # caso normal: refrescar lista y mostrar confirmación
                reload_members()
                show_success(page, "🗑️ Miembro eliminado correctamente")
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"), bgcolor="#A93226")
                page.snack_bar.open = True
            finally:
                cerrar()

        actions = ft.Row(
           [
                ft.TextButton("Cancelar", on_click=lambda e: cerrar()),
                ft.ElevatedButton("Eliminar", bgcolor="#D9534F", on_click=confirmar),
            ],
           alignment=ft.MainAxisAlignment.END,
            spacing=12,
        )

        modal = ft.Container(
           bgcolor=ft.Colors.with_opacity(0.65, "#000000"),
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Container(
                width=520,
                height=200,
                padding=ft.padding.all(20),
                border_radius=10,
                bgcolor="#0B1418",
                content=ft.Column([ft.Row([title]), ft.Divider(height=8), body, ft.Container(height=12), actions], spacing=12),
            ),
        )

        page.overlay.append(modal)
        page.update()

    def construir_filas(miembros):
        filas = []

        for m in miembros:
            nombre_completo = f"{m.get('apellido', '')} {m.get('nombre', '')}".strip()
            codigo = m.get("id_usuario", "-")
            rol_actual = str(m.get("rol", "") or "ALUMNO").upper()
            es_admin = rol_actual == "ADMIN"

            # Botones de acción
            botones = []

            # Solo STAFF puede administrar
            if is_staff and not es_admin:
                botones.append(ft.IconButton(
                    icon=ft.Icons.ADMIN_PANEL_SETTINGS,
                    icon_color=COLOR_ACCENT,
                    tooltip="Asignar Admin",
                    on_click=lambda e, miembro=m: asignar_admin_accion(miembro),
                ))

            # Mostrar botón eliminar si soy staff (puedo eliminar a otros)
            # o si la fila corresponde a mí (permitir "salirme" aunque no sea staff)
            if is_staff or m.get("id_usuario") == current_user_id:
                # si es el mismo usuario, cambiar tooltip/icon si quieres diferenciar ("Salir del aula")
                tooltip = "Salir del aula" if m.get("id_usuario") == current_user_id else "Eliminar miembro"
                icon = ft.Icons.EXIT_TO_APP if m.get("id_usuario") == current_user_id else ft.Icons.DELETE
                botones.append(ft.IconButton(
                    icon=icon,
                    icon_color="#D9534F",
                    tooltip=tooltip,
                    on_click=lambda e, miembro=m: eliminar_miembro_accion(miembro),
                ))

            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(nombre_completo, color=COLOR_TEXT_PRIMARY)),
                        ft.DataCell(ft.Text(codigo, color=COLOR_TEXT_SECONDARY)),
                        # nueva celda de Rol
                        ft.DataCell(
                            ft.Text(
                                rol_actual.title(),  # "Admin", "Alumno", etc.
                                color=COLOR_ACCENT if es_admin else COLOR_TEXT_SECONDARY,
                                weight=ft.FontWeight.BOLD if es_admin else ft.FontWeight.NORMAL
                            )
                        ),
                        ft.DataCell(ft.Row(botones, spacing=5)),
                    ]
                )
            )

        return filas

    tabla_miembros = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Apellidos y Nombres", color=COLOR_TEXT_PRIMARY, weight="bold")),
            ft.DataColumn(ft.Text("Código", color=COLOR_TEXT_PRIMARY, weight="bold")),
            ft.DataColumn(ft.Text("Rol", color=COLOR_TEXT_PRIMARY, weight="bold")),
            ft.DataColumn(ft.Text("Acciones", color=COLOR_TEXT_PRIMARY, weight="bold")),
        ],
        rows=construir_filas(miembros_list),
        border=ft.border.all(1, COLOR_BORDER_CARD),
        heading_row_color=ft.Colors.with_opacity(0.15, COLOR_ACCENT),
        data_row_color={"hovered": COLOR_BG_CARD_HOVER},
        column_spacing=40,
        horizontal_margin=20,
        divider_thickness=1,
    )

    # función para refrescar la tabla
    def reload_members():
        nonlocal miembros_list
        miembros_list = obtener_miembros_de_aula(id_aula)
        tabla_miembros.rows = construir_filas(miembros_list)
        page.update()


    lista_miembros = ft.Container(
        expand=True,
        padding=20,
        content=tabla_miembros,
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
