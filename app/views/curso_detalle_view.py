import flet as ft

def crear_vista_curso_detalle(page: ft.Page, id_curso: int):
    """
    Retorna un Container con el detalle del curso seleccionado.
    Ideal para actualizar dinámicamente el contenido principal (lado derecho).
    """

    # 🔹 Simulación temporal (luego lo reemplazas con consulta a BD)
    curso_data = {
        "nombre": f"Curso {id_curso}",
    }

    # --- Título del curso ---
    titulo_curso = ft.Text(
        curso_data["nombre"],
        size=36,
        weight=ft.FontWeight.BOLD,
        color="#FFFFFF",
    )

    # --- Botón volver ---
    btn_volver = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_color="#E0E0E0",
        icon_size=24,
        style=ft.ButtonStyle(
            shape=ft.CircleBorder(),
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
        ),
        on_click=lambda e: page.go("/aula_dashboard"),  # puedes cambiarlo si solo quieres cerrar el detalle
    )

    # --- Botón home ---
    btn_home = ft.IconButton(
        icon=ft.Icons.HOME,
        icon_color="#E0E0E0",
        icon_size=24,
        style=ft.ButtonStyle(
            shape=ft.CircleBorder(),
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
        ),
        on_click=lambda e: page.go("/options"),
    )

    # --- Header superior ---
    header = ft.Row(
        [
            titulo_curso,
            ft.Container(expand=True),
            btn_volver,
            btn_home,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # --- Botones tipo tarjeta ---
    def boton_modulo(icono, texto, on_click=None):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Text(
                        texto,
                        size=18,
                        color="#E0E0E0",
                        weight=ft.FontWeight.W_500,
                    ),
                    ft.Icon(icono, color="#E0E0E0", size=28),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            width=450,
            height=70,
            bgcolor="#151515",
            border_radius=10,
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            border=ft.border.all(1, "#2A2A2A"),
            ink=True,
            animate=ft.Animation(150, "easeOut"),
            on_hover=lambda e: (
                setattr(e.control, "bgcolor", "#1E1E1E" if e.data == "true" else "#151515"),
                e.control.update(),
            ),
            on_click=on_click,
        )

    # --- Botones específicos ---
    btn_tareas = boton_modulo(
        ft.Icons.CHECKLIST,
        "TAREAS",
        on_click=lambda e: page.snack_bar.open if setattr(page.snack_bar, "content", ft.Text("Abrir tareas")) else None,
    )

    btn_silabus = boton_modulo(
        ft.Icons.DESCRIPTION,
        "SILABUS",
        on_click=lambda e: page.snack_bar.open if setattr(page.snack_bar, "content", ft.Text("Abrir silabus")) else None,
    )

    # --- Estructura principal ---
    contenido = ft.Column(
        [
            header,
            ft.Container(height=40),
            btn_tareas,
            btn_silabus,
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.START,
    )

    # --- Container final (retornado) ---
    return ft.Container(
        content=contenido,
        alignment=ft.alignment.top_center,
        padding=ft.padding.all(40),
        expand=True,
        bgcolor="#000000",
    )
