import flet as ft
from datetime import datetime
from app.controllers.tareas_controller import obtener_tareas_por_aula
from app.controllers.anuncios_controller import crear_anuncio, obtener_anuncios_por_aula, actualizar_anuncio
from app.controllers.aulas_controller import obtener_aula_by_id
from app.utils.vald_text_fields import validar_formulario
from app.utils.is_staff_verification import is_staff_verification


def AnunciosAulaView(page: ft.Page, id_aula: int):
    # ------------------------------------------------------
    # CONFIGURACIÓN DE PÁGINA
    # ------------------------------------------------------
    page.title = "uniRed | Anuncios"
    page.scroll = ft.ScrollMode.AUTO
    is_staff = is_staff_verification(page, id_aula)
    edit_mode = False
    editing_course_id = None

    # 🎨 Paleta de colores coherente con todo el dashboard
    COLOR_BG_CARD = "#0E1E25"
    COLOR_BG_CARD_HOVER = "#152B33"
    COLOR_BORDER_CARD = "#1F3A44"
    COLOR_ACCENT = "#1C8DB0"
    COLOR_TEXT_PRIMARY = "#EAEAEA"
    COLOR_TEXT_SECONDARY = "#AAB6B8"

    # ------------------------------------------------------
    # --- CAMPOS DEL MODAL ---
    # ------------------------------------------------------
    titulo_input = ft.TextField(
        label="Título",
        bgcolor="#0D1A20",
        border_radius=8,
        border_color="#1F3A44",
        focused_border_color=COLOR_ACCENT,
        color=COLOR_TEXT_PRIMARY,
    )

    descripcion_input = ft.TextField(
        label="Descripción",
        bgcolor="#0D1A20",
        border_radius=8,
        border_color="#1F3A44",
        focused_border_color=COLOR_ACCENT,
        color=COLOR_TEXT_PRIMARY,
        multiline=True,
        min_lines=3,
        max_lines=6,
    )

    modal_title = ft.Text("CREAR ANUNCIO", weight=ft.FontWeight.BOLD, size=22, color="#FFFFFF")
    campos = [titulo_input, descripcion_input]

    # ------------------------------------------------------
    # --- FUNCIONES AUXILIARES ---
    # ------------------------------------------------------
    def _fmt_fecha(fecha):
        if not fecha:
            return ""
        if isinstance(fecha, datetime):
            return fecha.strftime("%d/%m/%Y %H:%M")
        try:
            dt = datetime.fromisoformat(str(fecha))
            return dt.strftime("%d/%m/%Y %H:%M")
        except Exception:
            try:
                dt = datetime.strptime(str(fecha), "%Y-%m-%d %H:%M:%S")
                return dt.strftime("%d/%m/%Y %H:%M")
            except Exception:
                return str(fecha)

    # ------------------------------------------------------
    # --- FUNCIONES MODAL ---
    # ------------------------------------------------------
    def validar_y_crear_tarea(e):
        nonlocal edit_mode, editing_course_id, lista_anuncios_col
        if not validar_formulario(page, campos):
            return

        try:
            if edit_mode:
                actualizar_anuncio(editing_course_id, titulo_input.value, descripcion_input.value)
            else:
                crear_anuncio(id_aula, titulo_input.value, descripcion_input.value)
            reload_anuncios()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"⚠ Error al guardar: {ex}"))
            page.snack_bar.open = True
            page.update()
            return

        cerrar_modal(e)
        page.snack_bar = ft.SnackBar(ft.Text("✅ Anuncio guardado correctamente"))
        page.snack_bar.open = True
        page.update()

    def abrir_modal(e):
        modal_container.visible = True
        page.update()

    def cerrar_modal(e):
        nonlocal edit_mode, editing_course_id
        modal_container.visible = False
        titulo_input.value = descripcion_input.value = ""
        edit_mode = False
        editing_course_id = None
        modal_title.value = "CREAR ANUNCIO"
        page.update()

    btn_guardar = ft.Container(
        content=ft.Text("Guardar", color="#FFFFFF", size=16, weight=ft.FontWeight.W_500),
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
        on_click=validar_y_crear_tarea,
    )

    btn_cancelar = ft.Container(
        content=ft.Text("Cancelar", color=COLOR_TEXT_SECONDARY, size=16),
        width=120,
        height=45,
        border_radius=8,
        alignment=ft.alignment.center,
        ink=True,
        border=ft.border.all(1, "#2C2C2C"),
        on_click=cerrar_modal,
    )

    form_container = ft.Container(
        width=700,
        height=420,
        bgcolor="#0B1418",
        border_radius=12,
        padding=30,
        border=ft.border.all(1, "#1E2C30"),
        content=ft.Column(
            [
                ft.Row([ft.Icon(ft.Icons.ADD_BOX_OUTLINED, color=COLOR_ACCENT), modal_title], spacing=10),
                ft.Divider(height=10, color="transparent"),
                titulo_input,
                descripcion_input,
                ft.Container(height=10),
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

    # ------------------------------------------------------
    # --- HEADER ---
    # ------------------------------------------------------
    nombre_aula = obtener_aula_by_id(id_aula)["nombre_aula"]

    titulo = ft.Text(
        f"Anuncios - {nombre_aula}",
        size=32,
        weight=ft.FontWeight.BOLD,
        color=COLOR_TEXT_PRIMARY,
    )

    btn_agregar = ft.Container(
        content=ft.Row(
            [ft.Icon(ft.Icons.ADD, color="#FFFFFF"), ft.Text("Nuevo anuncio", color="#FFFFFF")],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=6,
        ),
        gradient=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=[COLOR_ACCENT, "#186678"],
        ),
        width=180,
        height=45,
        border_radius=8,
        ink=True,
        visible=is_staff,
        on_click=abrir_modal,
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
        [titulo, ft.Container(expand=True), btn_agregar, btn_home],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # ------------------------------------------------------
    # --- TARJETAS ---
    # ------------------------------------------------------
    def card_anuncio(nombre, descripcion, fecha):
        expanded = ft.Ref[bool]()
        expanded.current = False
        desc_text = ft.Text(descripcion, color="#C7D3D4", size=14, visible=False)
        fecha_txt = ft.Text(fecha, size=12, color="#91A0A2")
        icono = ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, color="#C7D3D4")

        def toggle(e):
            expanded.current = not expanded.current
            desc_text.visible = expanded.current
            icono.name = ft.Icons.KEYBOARD_ARROW_UP if expanded.current else ft.Icons.KEYBOARD_ARROW_DOWN
            cont.update()

        cont = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.CAMPAIGN, color=COLOR_ACCENT),
                            ft.Text(nombre, size=17, color=COLOR_TEXT_PRIMARY, weight=ft.FontWeight.W_500),
                            ft.Container(expand=True),
                            ft.IconButton(icon=icono.name, icon_color="#CCCCCC", on_click=toggle),
                        ]
                    ),
                    desc_text,
                    fecha_txt,
                ],
                spacing=6,
            ),
            border_radius=10,
            padding=15,
            width=400,
            border=ft.border.all(1, COLOR_BORDER_CARD),
            bgcolor=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLOR_BG_CARD, "#0C252D"],
            ),
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
        return cont

    def card_tarea(nombre, nombre_curso, descripcion, fecha):
        expanded = ft.Ref[bool]()
        expanded.current = False
        desc_col = ft.Column(
            [
                ft.Text(f"Curso: {nombre_curso}", color="#B2C2C4", size=13),
                ft.Text(descripcion, color="#C7D3D4", size=14),
                ft.Text(f"Fecha Límite: {fecha}", color="#9CAAAA", size=13),
            ],
            spacing=4,
            visible=False,
        )
        icono = ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, color="#CCCCCC")

        def toggle(e):
            expanded.current = not expanded.current
            desc_col.visible = expanded.current
            icono.name = ft.Icons.KEYBOARD_ARROW_UP if expanded.current else ft.Icons.KEYBOARD_ARROW_DOWN
            card.update()

        card = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.DESCRIPTION, color=COLOR_ACCENT),
                            ft.Text(nombre, size=17, color=COLOR_TEXT_PRIMARY, weight=ft.FontWeight.W_500),
                            ft.Container(expand=True),
                            ft.IconButton(icon=icono.name, icon_color="#CCCCCC", on_click=toggle),
                        ]
                    ),
                    desc_col,
                ],
                spacing=6,
            ),
            border_radius=10,
            padding=15,
            width=400,
            border=ft.border.all(1, COLOR_BORDER_CARD),
            bgcolor=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=[COLOR_BG_CARD, "#0C252D"],
            ),
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
        return card

    # ------------------------------------------------------
    # --- LISTAS ---
    # ------------------------------------------------------
    lista_anuncios_col = ft.Column([], spacing=15, scroll=ft.ScrollMode.AUTO, expand=True)
    lista_tareas_col = ft.Column(
        [
            card_tarea(c["titulo"], c["nombre_curso"], c["descripcion"], c["fecha_entrega"])
            for c in obtener_tareas_por_aula(id_aula)
        ],
        spacing=15,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    def reload_anuncios():
        anuncios = obtener_anuncios_por_aula(id_aula)
        lista_anuncios_col.controls = [
            card_anuncio(c["titulo"], c["descripcion"], _fmt_fecha(c.get("fecha_publicacion")))
            for c in anuncios
        ]
        page.update()

    reload_anuncios()

    # ------------------------------------------------------
    # --- ESTRUCTURA PRINCIPAL ---
    # ------------------------------------------------------
    columnas = ft.Row(
        [lista_anuncios_col, ft.VerticalDivider(width=1, color="#2B2B2B"), lista_tareas_col],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True,
    )

    layout = ft.Container(
        content=ft.Column([header, ft.Container(height=20), columnas], spacing=20, expand=True),
        padding=ft.padding.all(40),
        expand=True,
    )

    # Fondo con degradado coherente al dashboard
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
