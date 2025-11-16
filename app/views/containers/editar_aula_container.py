import flet as ft
from app.controllers.aulas_controller import actualizar_aula
from app.utils.vald_text_fields import validar_formulario
from app.controllers.aulas_usuario_controller import obtener_rol_usuario_en_aula, agregar_usuario_a_aula
from app.utils.is_staff_verification import is_staff_verification
from app.utils.show_succes import show_success


def EditarAulaView(page: ft.Page, func_load_content, aula_dict: dict = None, on_update=None):
    """
    Vista rediseñada con estilo coherente al dashboard dark-petróleo.
    """

    # ------------------------------------------------------
    # CONFIGURACIÓN
    # ------------------------------------------------------
    page.title = "UniRed | Editar Aula"
    page.scroll = ft.ScrollMode.AUTO

    # Paleta coherente con las demás vistas
    COLOR_BG_CARD = "#0E1E25"
    COLOR_BG_CARD_HOVER = "#152B33"
    COLOR_BORDER_CARD = "#1F3A44"
    COLOR_ACCENT = "#1C8DB0"
    COLOR_TEXT_PRIMARY = "#EAEAEA"
    COLOR_TEXT_SECONDARY = "#AAB6B8"

    # ------------------------------------------------------
    # DATOS DEL AULA
    # ------------------------------------------------------
    nombre_val = aula_dict["nombre_aula"] if aula_dict else ""
    descripcion_val = aula_dict["descripcion"] if aula_dict else ""
    is_staff = is_staff_verification(page, aula_dict["id_aula"])

    # ------------------------------------------------------
    # CABECERA
    # ------------------------------------------------------
    titulo = ft.Text(
        "Editar Aula",
        size=36,
        weight=ft.FontWeight.BOLD,
        color=COLOR_TEXT_PRIMARY,
    )

    btn_home = ft.IconButton(
        icon=ft.Icons.HOME,
        icon_color="#EAEAEA",
        icon_size=26,
        style=ft.ButtonStyle(
            shape=ft.CircleBorder(),
            bgcolor=ft.Colors.with_opacity(0.1, "#1C8DB0"),
        ),
        tooltip="Volver al inicio",
        on_click=lambda e: page.go("/options"),
    )

    header = ft.Row(
        [titulo, ft.Container(expand=True), btn_home],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # ------------------------------------------------------
    # CAMPOS DE TEXTO
    # ------------------------------------------------------
    nombre_aula = ft.TextField(
        label="Nombre del Aula",
        hint_text="Ejemplo: AULA 203",
        bgcolor="#0D1A20",
        border_radius=8,
        border_color="#1F3A44",
        focused_border_color=COLOR_ACCENT,
        color=COLOR_TEXT_PRIMARY,
        width=400,
        value=nombre_val,
    )

    descripcion_aula = ft.TextField(
        label="Descripción del Aula",
        hint_text="Ejemplo: Laboratorio de programación",
        bgcolor="#0D1A20",
        border_radius=8,
        border_color="#1F3A44",
        focused_border_color=COLOR_ACCENT,
        color=COLOR_TEXT_PRIMARY,
        width=400,
        value=descripcion_val,
        multiline=True,
        min_lines=2,
        max_lines=5,
    )

    # ------------------------------------------------------
    # ACCIONES
    # ------------------------------------------------------
    def confirmar(e):
        actualizar_aula(
            id_aula=aula_dict["id_aula"],
            nombre_aula=nombre_aula.value,
            descripcion=descripcion_aula.value,
        )

        aula_dict["nombre_aula"] = nombre_aula.value
        aula_dict["descripcion"] = descripcion_aula.value

        # actualizar sesión
        try:
            page.session.set("selected_aula", aula_dict)
            page.session.set("selected_aula_id", int(aula_dict.get("id_aula")))
        except Exception:
            pass

        # feedback visual
        show_success(page, "Cambios guardados ✔")

        # callback para refrescar dashboard
        if callable(on_update):
            try:
                on_update(aula_dict)
            except Exception:
                pass
        else:
            page.go("/aula_dashboard")

        page.update()

    btn_confirmar = ft.Container(
        content=ft.Text("Guardar Cambios", color="#FFFFFF", size=16, weight=ft.FontWeight.W_500),
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=[COLOR_ACCENT, "#145C70"],
        ),
        width=220,
        height=45,
        border_radius=8,
        alignment=ft.alignment.center,
        ink=True,
        visible=is_staff,
        on_click=confirmar,
    )

    btn_miembros = ft.Container(
        content=ft.Row(
            [ft.Icon(ft.Icons.GROUP, color="#FFFFFF"), ft.Text("Ver Miembros", color="#FFFFFF")],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=6,
        ),
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=["#186678", COLOR_ACCENT],
        ),
        width=220,
        height=45,
        border_radius=8,
        ink=True,
        on_click=lambda e: func_load_content("Miembros"),
    )

    # ------------------------------------------------------
    # DIVISOR VISUAL
    # ------------------------------------------------------
    linea_div = ft.Container(
        height=1,
        bgcolor="#2B3A3F",
        width=450,
        border_radius=1,
        opacity=0.6,
    )

    # ------------------------------------------------------
    # LAYOUT PRINCIPAL
    # ------------------------------------------------------
    contenido = ft.Column(
        [
            header,
            ft.Container(height=40),
            nombre_aula,
            descripcion_aula,
            ft.Container(height=20),
            btn_confirmar,
            linea_div,
            btn_miembros,
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
    )

    layout = ft.Container(
        content=contenido,
        padding=ft.padding.all(50),
        expand=True,
        alignment=ft.alignment.top_left,
    )

    # Fondo con degradado igual al dashboard
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
        ],
        expand=True,
    )
