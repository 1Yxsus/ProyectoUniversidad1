import flet as ft
from datetime import datetime
from app.controllers.tareas_controller import obtener_tareas_por_aula
from app.controllers.anuncios_controller import crear_anuncio, obtener_anuncios_por_aula, actualizar_anuncio
from app.controllers.aulas_controller import obtener_aula_by_id
from app.utils.vald_text_fields import validar_formulario
from app.utils.is_staff_verification import is_staff_verification
from app.utils.show_succes import show_success


def AnunciosAulaView(page: ft.Page, id_aula: int):

    # =====================================================================
    # CONFIGURACIÓN DE PÁGINA
    # =====================================================================
    page.title = "uniRed | Anuncios"
    page.scroll = ft.ScrollMode.AUTO
    is_staff = is_staff_verification(page, id_aula)

    # 🎨 PALETA
    COLOR_BG_CARD = "#0E1E25"
    COLOR_BG_HOVER = "#152B33"
    COLOR_BORDER = "#1F3A44"
    COLOR_ACCENT = "#1C8DB0"
    COLOR_TEXT = "#EAEAEA"
    COLOR_SUBTEXT = "#AAB6B8"

    # =====================================================================
    # MODAL CREAR / EDITAR ANUNCIO
    # =====================================================================
    titulo_input = ft.TextField(
        label="Título", bgcolor="#0D1A20", border_radius=8,
        border_color=COLOR_BORDER, focused_border_color=COLOR_ACCENT,
        color=COLOR_TEXT
    )
    descripcion_input = ft.TextField(
        label="Descripción", bgcolor="#0D1A20", border_radius=8,
        border_color=COLOR_BORDER, focused_border_color=COLOR_ACCENT,
        color=COLOR_TEXT, multiline=True, min_lines=3, max_lines=6
    )

    modal_title = ft.Text("CREAR ANUNCIO", size=24, weight=ft.FontWeight.BOLD)

    def abrir_modal(e):
        modal_container.visible = True
        page.update()

    def cerrar_modal(e):
        modal_container.visible = False
        titulo_input.value = ""
        descripcion_input.value = ""
        page.update()

    def validar_crear(e):
        if not validar_formulario(page, [titulo_input, descripcion_input]):
            return
        crear_anuncio(id_aula, titulo_input.value, descripcion_input.value)
        reload_anuncios()
        cerrar_modal(e)
        show_success(page, "✅ Anuncio creado correctamente")
        page.update()

    modal_container = ft.Container(
        visible=False,
        expand=True,
        alignment=ft.alignment.center,
        bgcolor=ft.Colors.with_opacity(0.65, "#000"),
        content=ft.Container(
            width=600,
            height=350,
            padding=30,
            bgcolor="#0B1418",
            border_radius=12,
            border=ft.border.all(1, COLOR_BORDER),
            content=ft.Column(
                [
                    ft.Row(
                        [ft.Icon(ft.Icons.ADD_BOX, color=COLOR_ACCENT), modal_title,
                         ft.Container(expand=True),
                         ft.IconButton(icon=ft.Icons.CLOSE, on_click=cerrar_modal)],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    titulo_input,
                    descripcion_input,
                    ft.Row(
                        [
                            ft.ElevatedButton("Cancelar", on_click=cerrar_modal),
                            ft.ElevatedButton("Guardar", bgcolor=COLOR_ACCENT, on_click=validar_crear)
                        ],
                        alignment=ft.MainAxisAlignment.END
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                spacing=15,
            )
        )
    )

    # =====================================================================
    # HEADER
    # =====================================================================
    nombre_aula = obtener_aula_by_id(id_aula)["nombre_aula"]

    header = ft.Row(
        [
            ft.Text(f"Anuncios - {nombre_aula}", size=32, weight=ft.FontWeight.BOLD, color=COLOR_TEXT),
            ft.Container(expand=True),
            ft.Container(
                content=ft.Row(
                    [ft.Icon(ft.Icons.ADD, color="white"), ft.Text("Nuevo anuncio", color="white")],
                    spacing=8
                ),
                bgcolor=COLOR_ACCENT,
                padding=12,
                border_radius=8,
                visible=is_staff,
                ink=True,
                on_click=abrir_modal
            ),
            ft.IconButton(icon=ft.Icons.HOME, icon_color="white", on_click=lambda e: page.go("/options"))
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # =====================================================================
    # TARJETAS
    # =====================================================================
    def card_anuncio(titulo, desc, fecha):
        detail = ft.Text(desc, visible=False, color="#C7D3D4")
        arrow = ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, color="#aaa")

        def toggle(e):
            detail.visible = not detail.visible
            arrow.name = ft.Icons.KEYBOARD_ARROW_UP if detail.visible else ft.Icons.KEYBOARD_ARROW_DOWN
            card.update()

        card = ft.Container(
            padding=15,
            border_radius=10,
            border=ft.border.all(1, COLOR_BORDER),
            bgcolor=COLOR_BG_CARD,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.CAMPAIGN, color=COLOR_ACCENT),
                            ft.Text(titulo, size=17, weight=ft.FontWeight.W_500, color=COLOR_TEXT),
                            ft.Container(expand=True),
                            ft.IconButton(icon=arrow.name, icon_color="white", on_click=toggle)
                        ]
                    ),
                    detail,
                    ft.Text(fecha, size=12, color="#9EB3B3")
                ],
                spacing=6
            )
        )
        return card

    def card_tarea(nombre, curso, desc, fecha):
        detail = ft.Column(
            [
                ft.Text(f"Curso: {curso}", color="#9EB3B3"),
                ft.Text(desc, color="#C7D3D4"),
                ft.Text(f"Fecha: {fecha}", color="#9EB3B3"),
            ],
            visible=False
        )
        arrow = ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN)

        def toggle(e):
            detail.visible = not detail.visible
            arrow.name = ft.Icons.KEYBOARD_ARROW_UP if detail.visible else ft.Icons.KEYBOARD_ARROW_DOWN
            card.update()

        card = ft.Container(
            padding=15,
            border_radius=10,
            border=ft.border.all(1, COLOR_BORDER),
            bgcolor=COLOR_BG_CARD,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.DESCRIPTION, color=COLOR_ACCENT),
                            ft.Text(nombre, size=17, weight=ft.FontWeight.W_500, color=COLOR_TEXT),
                            ft.Container(expand=True),
                            ft.IconButton(icon=arrow.name, on_click=toggle)
                        ]
                    ),
                    detail,
                ],
                spacing=6
            )
        )
        return card

    # =====================================================================
    # CLASIFICAR TAREAS
    # =====================================================================
    tareas = obtener_tareas_por_aula(id_aula)

    def parse_dt(v):
        if isinstance(v, datetime):
            return v
        try:
            return datetime.fromisoformat(str(v))
        except:
            return None

    now = datetime.now()
    pendientes = []
    expiradas = []

    for t in tareas:
        dt = parse_dt(t.get("fecha_entrega"))
        if dt and dt < now:
            expiradas.append(t)
        else:
            pendientes.append(t)

    # =====================================================================
    # COLUMNAS CON SCROLL INDEPENDIENTE + DISEÑO RESPONSIVO
    # =====================================================================

    anuncios_list = ft.Column([], spacing=15, expand=True, scroll=ft.ScrollMode.AUTO)

    def empty_placeholder(title: str, subtitle: str = "", icon=ft.Icons.INFO_OUTLINE):
        return ft.Container(
            padding=20,
            border_radius=8,
            border=ft.border.all(1, COLOR_BORDER),
            bgcolor=ft.Colors.with_opacity(0.02, "white"),
            content=ft.Column(
                [
                    ft.Row([ft.Icon(icon, color=COLOR_ACCENT), ft.Text(title, color=COLOR_TEXT, weight=ft.FontWeight.BOLD)]),
                    ft.Container(height=8),
                    ft.Text(subtitle, color=COLOR_SUBTEXT),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )
    # altura mínima para las columnas de contenido para evitar colapsos
    MIN_SECTION_HEIGHT = 260

    def _fmt_fecha(val):
        """Formatea diferentes inputs de fecha a 'DD/MM/YYYY HH:MM' o devuelve str(val) si no se puede parsear."""
        if not val:
            return ""
        if isinstance(val, datetime):
            dt = val
        else:
            s = str(val).strip()
            # intentar ISO primero
            try:
                dt = datetime.fromisoformat(s)
            except Exception:
                dt = None
                # formatos comunes
                for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d", "%d/%m/%Y %H:%M", "%d/%m/%Y"):
                    try:
                        dt = datetime.strptime(s, fmt)
                        break
                    except Exception:
                        continue
            if dt is None:
                return s
        try:
            return dt.strftime("%d/%m/%Y %H:%M")
        except Exception:
            return str(val)

    def reload_anuncios():
        anuncios = obtener_anuncios_por_aula(id_aula)
        if not anuncios:
            anuncios_list.controls = [empty_placeholder("No hay anuncios", "Aquí se mostrarán los anuncios del curso.")]
        else:
            anuncios_list.controls = [
                card_anuncio(a["titulo"], a["descripcion"], _fmt_fecha(a["fecha_publicacion"]))
                for a in anuncios
            ]
        page.update()

    reload_anuncios()

    left_section = ft.Container(
        bgcolor="#111A1F",
        padding=20,
        border_radius=12,
        expand=True,
        content=ft.Column(
            [
                 ft.Text("Anuncios", size=22, color="white", weight=ft.FontWeight.BOLD),
                 ft.Container(height=10),
                 ft.Container(content=anuncios_list,
                    expand=True,
                    height=MIN_SECTION_HEIGHT,
                    border_radius=8,
                    padding=5,
                    bgcolor=ft.Colors.with_opacity(0.02, "white"),
                )
            ],
            expand=True
        )
    )

    # función auxiliar para crear la columna de tareas (con placeholder y altura mínima)
    def build_tasks_col(title, tasks, empty_msg, highlight=False):
        items = []
        if not tasks:
            items = [empty_placeholder(empty_msg, "No hay tareas en esta categoría.", icon=ft.Icons.DESCRIPTION)]
        else:
            items = [card_tarea(t["titulo"], t.get("nombre_curso", ""), t.get("descripcion", ""), _fmt_fecha(t.get("fecha_entrega"))) for t in tasks]

        color = "#111A1F"
        title_color = "#FF8080" if highlight else "white"
        return ft.Container(
            bgcolor=color,
            padding=20,
            border_radius=12,
            expand=True,
            content=ft.Column(
                [
                    ft.Text(title, size=20, color=title_color, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        expand=True,
                        padding=5,
                        content=ft.Container(
                            content=ft.Column(items, spacing=15, expand=True, scroll=ft.ScrollMode.AUTO),
                            height=MIN_SECTION_HEIGHT,
                            border_radius=8,
                            padding=6,
                            bgcolor=ft.Colors.with_opacity(0.02, "white"),
                        )
                    )
                ],
                expand=True,
            )
        )

    pendientes_section = build_tasks_col("Tareas Pendientes", pendientes, "No hay tareas pendientes")
 

    expiradas_section = build_tasks_col("Tareas Expiradas", expiradas, "No hay tareas expiradas", highlight=True)
 

    right_section = ft.Column(
        [
            pendientes_section,
            expiradas_section
        ],
        spacing=20,
        expand=True,
    )

    columnas = ft.Row(
        [
            ft.Container(content=left_section, width=420),
            ft.VerticalDivider(width=1, color="#2C2C2C"),
            ft.Container(content=right_section, expand=True),
        ],
        expand=True
    )

    # =====================================================================
    # LAYOUT FINAL
    # =====================================================================
    return ft.Stack(
        [
            ft.Container(
                gradient=ft.LinearGradient(
                    colors=["#0C1C24", "#0E2329", "#08171C"],
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                ),
                expand=True
            ),
            ft.Container(
                padding=40,
                content=ft.Column([header, ft.Container(height=20), columnas], expand=True),
                expand=True,
            ),
            modal_container,
        ],
        expand=True
    )
