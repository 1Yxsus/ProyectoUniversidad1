import flet as ft
from app.controllers.aulas_controller import obtener_aulas
from app.controllers.aulas_usuario_controller import obtener_roles_por_usuario


def AulasView(page: ft.Page, aulas_propias=None, aulas_invitado=None):
    """
    Vista estilizada dark-petróleo para mostrar las aulas del usuario.
    """

    # ================================
    # COLORES BASE
    # ================================
    COLOR_ACCENT = "#1C8DB0"
    COLOR_BG_CARD = "#0E1E25"
    COLOR_BG_HOVER = "#152B33"
    COLOR_BORDER = "#1F3A44"
    COLOR_TEXT = "#EAEAEA"
    COLOR_TEXT_SEC = "#AAB6B8"

    # ================================
    # CONFIGURACIÓN GENERAL
    # ================================
    page.title = "UniversApp | Mis Aulas"
    page.bgcolor = "#000000"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    # ================================
    # DATOS DEL USUARIO
    # ================================
    current_user = page.session.get("user") or {}
    uid = current_user.get("id_usuario")

    if aulas_propias is None and aulas_invitado is None:
        aulas_usuario = obtener_aulas(uid) if uid else []
        aulas_propias = [a for a in aulas_usuario if str(a.get("rol", "")).upper() == "ADMIN"]
        aulas_invitado = [a for a in aulas_usuario if str(a.get("rol", "")).upper() != "ADMIN"]
    else:
        aulas_propias = aulas_propias or []
        aulas_invitado = aulas_invitado or []

    # ================================
    # BOTÓN HOME
    # ================================
    btn_home = ft.IconButton(
        icon=ft.Icons.HOME,
        icon_color=COLOR_TEXT,
        style=ft.ButtonStyle(shape=ft.CircleBorder(), bgcolor="#122A33"),
        tooltip="Inicio",
        on_click=lambda e: page.go("/options"),
    )

    # ================================
    # TARJETAS DE AULA
    # ================================
    def crear_card_aula(aula):
        nombre = aula.get("nombre_aula") or aula.get("nombre") or str(aula)
        descripcion = aula.get("descripcion") or aula.get("desc") or ""

        def abrir_aula(e):
            page.session.set("selected_aula", aula)
            page.session.set("selected_aula_id", aula.get("id_aula") or aula.get("id") or None)
            page.go("/aula_dashboard")

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        nombre,
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=COLOR_TEXT,
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                    ft.Text(
                        descripcion,
                        size=13,
                        color=COLOR_TEXT_SEC,
                        max_lines=2,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                ],
                spacing=6,
            ),
            width=250,
            height=110,
            border=ft.border.all(1, COLOR_BORDER),
            border_radius=12,
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
            bgcolor=ft.LinearGradient(colors=[COLOR_BG_CARD, "#0C252D"]),
            ink=True,
            animate=ft.Animation(180, "easeOut"),
            on_click=abrir_aula,
            on_hover=lambda e: (
                setattr(
                    e.control,
                    "bgcolor",
                    ft.LinearGradient(colors=[COLOR_BG_HOVER, "#133540"])
                    if e.data == "true"
                    else ft.LinearGradient(colors=[COLOR_BG_CARD, "#0C252D"]),
                ),
                e.control.update(),
            ),
        )

    # ================================
    # GENERADOR DE FILAS
    # ================================
    def generar_filas(aulas):
        if not aulas:
            return [ft.Text("No hay aulas disponibles", color=COLOR_TEXT_SEC, size=14)]

        filas = []
        fila_actual = []
        for i, aula in enumerate(aulas, 1):
            fila_actual.append(crear_card_aula(aula))
            if i % 4 == 0 or i == len(aulas):
                filas.append(ft.Row(controls=fila_actual, spacing=20))
                fila_actual = []
        return filas

    # ================================
    # SECCIONES
    # ================================
    propiedad_titulo = ft.Text("Aulas Propias", size=32, weight=ft.FontWeight.BOLD, color=COLOR_TEXT)
    invitado_titulo = ft.Text("Aulas Invitado", size=32, weight=ft.FontWeight.BOLD, color=COLOR_TEXT)

    propiedad_grid = generar_filas(aulas_propias)
    invitado_grid = generar_filas(aulas_invitado)

    # ================================
    # CONTENIDO SCROLL
    # ================================
    contenido_scroll = ft.Container(
        expand=True,
        content=ft.Column(
            [
                propiedad_titulo,
                *propiedad_grid,
                ft.Container(height=40),
                invitado_titulo,
                *invitado_grid,
            ],
            spacing=25,
            scroll=ft.ScrollMode.AUTO,
        ),
    )

    # ================================
    # ESTRUCTURA PRINCIPAL
    # ================================
    contenido = ft.Column(
        [
            ft.Row(
                [ft.Text("Mis Aulas", size=38, color=COLOR_TEXT, weight=ft.FontWeight.BOLD), ft.Container(expand=True), btn_home],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Container(height=20),
            contenido_scroll,
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.START,
    )

    # ================================
    # LAYOUT FINAL
    # ================================
    layout = ft.Container(
        expand=True,
        padding=ft.padding.all(50),
        content=contenido,
        alignment=ft.alignment.top_left,
    )

    return ft.Container(
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#0C1C24", "#0E2329", "#08171C"],
        ),
        content=layout,
        expand=True,
    )
