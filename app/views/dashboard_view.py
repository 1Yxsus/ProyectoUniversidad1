import flet as ft

def DashboardView(page: ft.Page, username: str = "Estudiante UNFV"):
    
    # --- Información de usuario ---
    user = page.session.get("user")

    if not user:
        page.go("/login")
        return

    id = user["id_usuario"]
    nombre = user["nombre"]
    apellido = user["apellido"]
    correo = user["correo"]
    fecha = user["fecha_registro"]

    # --- CONFIGURACIÓN GENERAL ---
    page.bgcolor = ft.Colors.BLACK
    page.padding = 0
    
    # Estado de la sección actual
    current_section = {"value": "cursos"}
    
    # Datos de ejemplo de cursos
    courses = [
        {"name": "Programación Aplicada", "teacher": "Prof. García", "code": "PA-2024"},
        {"name": "Base de Datos", "teacher": "Prof. Martínez", "code": "BD-2024"},
        {"name": "Ingeniería de Software", "teacher": "Prof. López", "code": "IS-2024"},
        {"name": "Algoritmos Avanzados", "teacher": "Prof. Rodríguez", "code": "AA-2024"},
    ]
    
    def create_sidebar_item(icon, text, section_id):
        """Crea un item de la barra lateral"""
        is_selected = current_section["value"] == section_id
        
        def on_click_section(e):
            current_section["value"] = section_id
            page.update()
        
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, color=ft.Colors.WHITE if is_selected else ft.Colors.GREY_400, size=20),
                    ft.Text(text, color=ft.Colors.WHITE if is_selected else ft.Colors.GREY_400, size=14),
                ],
                spacing=15,
            ),
            padding=15,
            bgcolor=ft.Colors.GREY_900 if is_selected else ft.Colors.BLACK,
            border_radius=8,
            on_click=on_click_section,
            ink=True,
        )
    
    def create_course_card(course):
        """Crea una tarjeta de curso"""
        def open_course(e):
            print(f"Abriendo curso: {course['name']}")
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Text(
                            course["name"][0],
                            size=40,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE,
                        ),
                        bgcolor=ft.Colors.BLUE_GREY_900,
                        height=120,
                        alignment=ft.alignment.center,
                        border_radius=ft.border_radius.only(top_left=8, top_right=8),
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    course["name"],
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE,
                                ),
                                ft.Text(
                                    course["teacher"],
                                    size=12,
                                    color=ft.Colors.GREY_400,
                                ),
                                ft.Text(
                                    course["code"],
                                    size=11,
                                    color=ft.Colors.GREY_500,
                                ),
                            ],
                            spacing=5,
                        ),
                        padding=15,
                    ),
                ],
                spacing=0,
            ),
            width=280,
            bgcolor=ft.Colors.GREY_900,
            border_radius=8,
            border=ft.border.all(1, ft.Colors.GREY_800),
            on_click=open_course,
            ink=True,
        )
    
    # Barra lateral
    sidebar = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=60, color=ft.Colors.WHITE),
                            ft.Text(username, size=16, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    padding=20,
                ),
                ft.Divider(color=ft.Colors.GREY_800, height=1),
                ft.Container(
                    content=ft.Column(
                        [
                            create_sidebar_item(ft.Icons.GRID_VIEW, "Cursos", "cursos"),
                            create_sidebar_item(ft.Icons.CALENDAR_TODAY, "Calendario", "calendario"),
                            create_sidebar_item(ft.Icons.ASSIGNMENT, "Tareas", "tareas"),
                            create_sidebar_item(ft.Icons.PEOPLE, "Personas", "personas"),
                            create_sidebar_item(ft.Icons.SETTINGS, "Configuración", "configuracion"),
                        ],
                        spacing=10,
                    ),
                    padding=ft.padding.only(left=20, right=20, top=20),
                ),
            ],
            spacing=0,
        ),
        width=250,
        bgcolor=ft.Colors.BLACK,
        padding=ft.padding.only(top=20, bottom=20),
    )
    
    # Área principal
    main_content = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Text(
                        "Mis Cursos",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                    ),
                    padding=ft.padding.only(left=30, top=30, bottom=20),
                ),
                ft.Container(
                    content=ft.Row(
                        [create_course_card(course) for course in courses],
                        spacing=20,
                        wrap=True,
                    ),
                    padding=ft.padding.only(left=30, right=30),
                ),
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
        ),
        bgcolor=ft.Colors.with_opacity(0.02, ft.Colors.WHITE),
        expand=True,
    )
    
    # Layout principal
    dashboard = ft.Row(
        [
            sidebar,
            ft.VerticalDivider(width=1, color=ft.Colors.GREY_900),
            main_content,
        ],
        spacing=0,
        expand=True,
    )
    
    return ft.Container(
        content=dashboard,
        expand=True,
        bgcolor=ft.Colors.BLACK,
    )


def main(page: ft.Page):
    page.title = "UniversApp - Dashboard"
    page.bgcolor = ft.Colors.BLACK
    page.padding = 0
    page.theme_mode = ft.ThemeMode.DARK
    
    dashboard = DashboardView(page, username="Estudiante UNFV")
    page.add(dashboard)


if __name__ == "__main__":
    ft.app(target=main)
