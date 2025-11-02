import flet as ft
from app.controllers.aulas_controller import crear_aulas

def DashboardOptionsView(page: ft.Page):

    # --- Información de usuario ---
    user = page.session.get("user")

    if not user:
        page.go("/login")
        return

    id = user["id_usuario"]
    nombre = user["nombre"]
    apellido = user["apellido"]

    # --- CONFIGURACIÓN GENERAL ---
    page.bgcolor = "#000000"  # Negro total
    page.title = "Panel Principal"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # --- BOTÓN DE CERRAR SESIÓN ---
    btn_logout = ft.TextButton(
        text="Cerrar Sesión",
        style=ft.ButtonStyle(
            bgcolor="#2B0000",  # Rojo oscuro
            color=ft.Colors.WHITE,
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
        on_click=lambda e: page.go("/login"),
    )

    logout_container = ft.Container(
        content=btn_logout,
        padding=ft.padding.only(right=40, top=10),  # separa del borde
    )

    # --- TÍTULO BIENVENIDA ---
    lbl_bienvenida = ft.Text(
        value=f"Bienvenido, {nombre} {apellido}",
        size=40,
        color=ft.Colors.WHITE,
        weight=ft.FontWeight.W_500,
        italic=True,
        text_align=ft.TextAlign.CENTER,
    )

    # --- TextFields del modal (Reutilizados) ---
    nombre_aula = ft.TextField(
        label="Nombre del Aula:",
        hint_text="Ejemplo: AULA 203",
        bgcolor="#1E1E1E",
        border_radius=10,
        border_color=ft.Colors.TRANSPARENT,
    )

    descripcion = ft.TextField(
        label="Descripción:",
        hint_text="Máximo 200 caracteres",
        bgcolor="#1E1E1E",
        border_radius=10,
        border_color=ft.Colors.TRANSPARENT,
        multiline=True,
    )

    # --- Funciones para abrir/cerrar el modal ---

    def abrir_modal(e):
        modal_container.visible = True
        page.update()

    def cerrar_modal(e):
        modal_container.visible = False
        # Opcional: limpiar campos al cerrar
        nombre_aula.value = ""
        descripcion.value = ""
        page.update()

    def crear_aula(e):

        crear_aulas(nombre_aula.value, descripcion.value, id)
        print(f"Aula Creada: {nombre_aula.value}")
        
        # Mostrar SnackBar (copiado de tu lógica original)
        page.snack_bar.content = ft.Text(f"Aula '{nombre_aula.value}' creada")
        page.snack_bar.open = True
        
        # Cerrar el modal
        cerrar_modal(e)

    # --- Botones del modal (Reutilizados y adaptados) ---
    btn_crear_modal = ft.ElevatedButton(
        text="CREAR",
        bgcolor="#2C2F3A",
        color=ft.Colors.WHITE,
        width=200,
        height=60,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        on_click=crear_aula, # <-- Conectado a la nueva función
    )
    
    # Es crucial añadir un botón para cancelar/cerrar
    btn_cancelar_modal = ft.TextButton(
        text="Cancelar",
        on_click=cerrar_modal # <-- Conectado a la función de cierre
    )

    # --- 1. El Formulario del Modal (El contenedor del centro) ---
    # Este es el contenedor que simula el 'AlertDialog'
    
    form_container = ft.Container(
        width=700,  # más ancho para forma rectangular
        height=400,
        bgcolor="#121212",
        border=ft.border.all(1, "#222222"),
        border_radius=12,
        padding=ft.padding.symmetric(horizontal=30, vertical=20),
        content=ft.Column(
            [
                # Header
                ft.Row(
                    [
                        ft.Icon(ft.Icons.ADD_BOX_OUTLINED, color=ft.Colors.WHITE),
                        ft.Text("CREAR AULA", weight=ft.FontWeight.BOLD, size=22),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Divider(height=8, color=ft.Colors.TRANSPARENT),

                # Inputs (ocupando todo el ancho disponible del formulario)
                ft.Column(
                    [
                        ft.Text("Nombre del Aula:", weight=ft.FontWeight.BOLD),
                        ft.Container(content=nombre_aula, width=640),
                        ft.Container(height=8),
                        ft.Text("Descripción:", weight=ft.FontWeight.BOLD),
                        ft.Container(content=descripcion, width=640, height=70),
                    ],
                    spacing=12,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                ),

                ft.Divider(height=5, color=ft.Colors.TRANSPARENT),

                # Acciones: alineadas a la derecha
                ft.Row(
                    [
                        ft.Container(expand=True),  # empuja los botones a la derecha
                        ft.Row(
                            [btn_cancelar_modal, btn_crear_modal],
                            spacing=12,
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            spacing=12,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        ),
    )

    # --- 2. El Contenedor Modal (El fondo gris/dimmer) ---
    # Este contenedor ocupa toda la pantalla y centra el formulario
    
    modal_container = ft.Container(
        # Fondo semi-transparente para "oscurecer" la app
        bgcolor=ft.Colors.with_opacity(0.6, ft.Colors.BLACK),
        
        # Ocupa todo el espacio disponible
        expand=True, 
        
        # Centra el 'form_container'
        alignment=ft.alignment.center, 
        
        # El contenido es el formulario que definimos arriba
        content=form_container,
        
        # EMPIEZA OCULTO
        visible=False,
    )


    # --- 4. Configuración Final de la Página ---
    
    # Preparamos el SnackBar (de tu código original)
    page.snack_bar = ft.SnackBar(content=ft.Text(""))

    # --- FUNCIÓN PARA CREAR BOTONES ---
    def create_button(icon, text, width=350, height=220, on_click=None):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, size=80, color=ft.Colors.WHITE),
                    ft.Text(text, size=28, color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor="#111111",  # Negro muy oscuro
            width=width,
            height=height,
            border_radius=15,
            alignment=ft.alignment.center,
            ink=True,
            on_click=on_click,
            border=ft.border.all(1, "#222222"),
        )

    # --- BOTONES IZQUIERDA Y DERECHA ---
    btn_crear_aula = create_button(ft.Icons.ADD, "Crear Aula", on_click=abrir_modal)
    btn_tus_aulas = create_button(ft.Icons.GROUP, "Tus Aulas", on_click=lambda e: page.go("/aula_dashboard"))
    # El botón de Herramientas ocupa el doble de alto
    btn_herramientas = create_button(
        ft.Icons.SETTINGS,
        "Herramientas",
        height=(220 * 2) + 20,  # alto de dos botones más espacio
        on_click=lambda e: page.go("/herramientas"),
        width=350,
    )

    # --- LAYOUT DE BOTONES ---
    botones = ft.Row(
        [
            ft.Column(
                [btn_crear_aula, btn_tus_aulas],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            btn_herramientas,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=40,
    )

    # --- CABECERA ---
    header = ft.Row(
        [
            ft.Container(expand=True),
            logout_container,
        ],
        alignment=ft.MainAxisAlignment.END,
    )

    # --- CONTENEDOR PRINCIPAL ---
    contenido = ft.Column(
        [
            header,
            lbl_bienvenida,
            ft.Container(height=30),
            botones,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    return ft.Container(
        content=ft.Stack(
            [
                # Elemento 1: El contenido principal (al fondo)
                contenido,
                
                # Elemento 2: El modal (encima)
                modal_container,
            ],
            # Hacemos que el Stack ocupe toda la página
            expand=True 
        ),
        alignment=ft.alignment.center,  # 👈 centra vertical y horizontal
        expand=True,                    # ocupa toda la pantalla
        bgcolor=ft.Colors.BLACK
    )
