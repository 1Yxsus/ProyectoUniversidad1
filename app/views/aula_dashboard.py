import flet as ft
from app.controllers.aulas_controller import obtener_aulas
from app.controllers.cursos_controller import crear_curso, obtener_cursos, actualizar_curso

def AulaDashboardView(page: ft.Page):
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

# ------------------------------------------------------
# Funciones Generales
# ----------------------------------------------------

    # estado para edición
    edit_mode = False
    editing_course_id = None

    def abrir_modal_para_editar(curso_dict):
        """
        Abre el modal y carga los datos del curso seleccionado.
        curso_dict: diccionario con al menos los campos identificadores y los nombres.
        """
        nonlocal edit_mode, editing_course_id
        # extraer id seguro
        editing_course_id = curso_dict.get("id_curso")
        nombre_curso.value = curso_dict.get("curso")
        docente.value = curso_dict.get("docente") or curso_dict.get("nombre_docente") or ""
        delegado.value = str(curso_dict.get("delegado_id") or curso_dict.get("id_delegado") or curso_dict.get("delegado") or "")

        edit_mode = True
        # actualizar UI del modal (titulo y botón)
        try:
            modal_title.value = "EDITAR CURSO"
        except Exception:
            pass
        try:
            btn_crear_modal.text = "GUARDAR"
        except Exception:
            pass
        modal_container.visible = True
        page.update()

    def cargar_cursos_por_aula(id_aula):
        cursos_list = obtener_cursos(selected_id)
        cards = [ course_card(c) for c in cursos_list ]

        cursos_grid = course_grid(cards, max_per_row=4)
        content.content.controls[2] = cursos_grid

    def actualizar_contenido(texto):
        actualizar_titulo(texto)

        if texto == "Cursos":
            cargar_cursos_por_aula(selected_id)
        elif texto == "Anuncios":
            content.content.controls[2] = ft.Text("Sección de Anuncios en construcción...", color=ft.Colors.WHITE)
        
        page.update()

    selected_id = None

    def on_aula_change(e):
        # e.control.value o dropdown_aula.value devuelve la 'key' (id) que asignamos
        nonlocal selected_id
        selected_id = int(e.control.value) if e.control and e.control.value else None
        print("Aula seleccionada id:", selected_id)

        cursos_list = obtener_cursos(selected_id)

        if not cursos_list:
            print("No hay cursos para el aula seleccionada.")
            content.content.controls[2] = ft.Text("No hay cursos disponibles para esta aula.", color=ft.Colors.WHITE)
            page.update()
            return

        cargar_cursos_por_aula(selected_id)
        page.update()

    def actualizar_titulo(texto):
        titulo_header.value = texto
        page.update()

    # --- CONFIGURACIÓN GENERAL ---
    page.bgcolor = "#000000"
    page.title = "Aula 365 | Cursos"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    

    list_aulas = obtener_aulas(id)
    
    # --- DESPLEGABLE DE AULA ---
    dropdown_aula = ft.Dropdown(
        value=str(list_aulas[0]["id_aula"]) if list_aulas else None,  # <-- usar id como value
        options=[
            ft.dropdown.Option(
                key=str(a['id_aula']),
                text=f"{a['nombre_aula']} - {a['id_aula']}"
            ) for a in list_aulas
        ],
        color=ft.Colors.WHITE,
        border_color="#333333",
        focused_border_color="#555555",
        width=150,
    )

# ------------------------------------------------------
# ---------------- TARJETA DE CURSO --------------------
# ------------------------------------------------------

    def course_card(curso_dict):
        nombre = curso_dict.get("curso")
        docente = curso_dict.get("docente")
        delegado = curso_dict.get("delegado")

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                expand=True,
                                content=ft.Text(
                                    nombre,
                                    size=18,
                                    weight=ft.FontWeight.W_500,
                                    color="#F1F1F1",
                                    max_lines=2,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                            ),
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                icon_color="#B0B0B0",
                                icon_size=20,
                                style=ft.ButtonStyle(
                                    shape=ft.CircleBorder(),
                                    overlay_color=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                                ),
                                on_click=lambda e, c=curso_dict: abrir_modal_para_editar(c),
                                tooltip="Editar curso",
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Text(f"Docente: {docente}", color="#A8A8A8", size=14),
                    ft.Text(f"Delegado: {delegado}", color="#A8A8A8", size=14),
                ],
                spacing=6,
                alignment=ft.MainAxisAlignment.START,
            ),
            width=320,
            height=150,
            bgcolor="#151515",
            border=ft.border.all(1, "#2B2B2B"),
            border_radius=10,
            padding=15,
            ink=True,
            animate=ft.Animation(150, "easeOut"),
            on_hover=lambda e: (
                setattr(e.control, "bgcolor", "#1E1E1E" if e.data == "true" else "#151515"),
                e.control.update(),
            ),
            on_click=lambda e, n=nombre: print(f"Abrir curso: {n}"),
        )



    # --- SIMULACIÓN DE GRID SIN WRAP ---
    # Creamos filas manualmente con Row dentro de un Column
    def course_grid(cards, max_per_row=3):
        rows = []
        for i in range(0, len(cards), max_per_row):
            fila = ft.Row(
                cards[i:i+max_per_row],
                spacing=20,
                alignment=ft.MainAxisAlignment.START,
            )
            rows.append(fila)

        return ft.Container(
            content=ft.Column(
                rows,
                spacing=20,
                alignment=ft.MainAxisAlignment.START,
            ),
        )
    
    cursos_grid = course_grid([], max_per_row=4)
      
# ------------------------------------------------------
# ---------------- ASIDE SECTION -----------------------
# ------------------------------------------------------

    # --- USUARIO (ICONO Y NOMBRE) ---
    user_info = ft.Column(
        [
            ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=70, color=ft.Colors.WHITE),
            ft.Text(f"{nombre} {apellido}", size=20, color=ft.Colors.LIGHT_BLUE_ACCENT, weight=ft.FontWeight.W_500),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5,
    )

    # --- BOTONES DE MENÚ IZQUIERDO ---

    def side_button(text, selected=False):
        base_color = "#1A1A1A"
        hover_color = "#2A2A2A"
        text_color = "#E0E0E0"

        container = ft.Container(
            content=ft.Text(
                text,
                color=text_color,
                size=17,
                weight=ft.FontWeight.W_400,
            ),
            width=160,
            height=45,
            alignment=ft.alignment.center,
            bgcolor=base_color,
            border_radius=8,
            border=ft.border.all(1, "#2E2E2E"),
            ink=True,
            animate=ft.Animation(200, "easeOut"),
            on_click=lambda e: actualizar_contenido(text),
        )

        container.on_hover = lambda e: (
            setattr(container, "bgcolor", hover_color if e.data == "true" else base_color),
            setattr(container, "border", ft.border.all(1, "#3A3A3A" if e.data == "true" else "#2E2E2E")),
            container.update()
        )
        return container



    btn_cursos = side_button("Cursos")
    btn_anuncios = side_button("Anuncios")

    btn_logout = ft.Container(
        content=ft.Text("Cerrar Sesión", color="#E0E0E0", size=16),
        width=160,
        height=45,
        alignment=ft.alignment.center,
        bgcolor="#201010",
        border_radius=8,
        border=ft.border.all(1, "#3A1A1A"),
        ink=True,
        on_click=lambda e: page.go("/login"),
        on_hover=lambda e: (
            setattr(e.control, "bgcolor", "#2C1414" if e.data == "true" else "#201010"),
            e.control.update(),
        ),
    )


    # --- SIDEBAR COMPLETO ---
    sidebar = ft.Container(
        width=200,
        bgcolor="#0A0A0A",
        padding=20,
        content=ft.Column(
            [
                dropdown_aula,
                ft.Container(height=30),
                user_info,
                ft.Container(height=30),
                btn_cursos,
                btn_anuncios,
                ft.Container(expand=True),
                btn_logout,
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )


# ------------------------------------------------------
# ------------------ MODAL CREAR CURSO ------------------
# ------------------------------------------------------

    # --- TextFields del modal (Reutilizados) ---
    nombre_curso = ft.TextField(
        label="Nombre del Curso:",
        hint_text="Ejemplo: AULA 203",
        bgcolor="#1E1E1E",
        border_radius=10,
        border_color=ft.Colors.TRANSPARENT,
    )

    docente = ft.TextField(
        label="Docente:",
        hint_text="Máximo 200 caracteres",
        bgcolor="#1E1E1E",
        border_radius=10,
        border_color=ft.Colors.TRANSPARENT,
        multiline=True,
    )

    delegado = ft.TextField(
        label="Delegado:",
        hint_text="ID Delegado",
        bgcolor="#1E1E1E",
        border_radius=10,
        border_color=ft.Colors.TRANSPARENT,
        multiline=True,
    )

    # título mutable del modal (se actualiza al editar)
    modal_title = ft.Text("CREAR CURSO", weight=ft.FontWeight.BOLD, size=22, color=ft.Colors.WHITE)

    # --- Botones del modal (Reutilizados y adaptados) ---
    def validar_y_crear_curso(e):
        valid = True

        if not nombre_curso.value or not nombre_curso.value.strip():
            nombre_curso.error_text = "Campo requerido"
            valid = False
        else:
            nombre_curso.error_text = None

        if not docente.value or not docente.value.strip():
            docente.error_text = "Campo requerido"
            valid = False
        else:
            docente.error_text = None

        if not delegado.value or not delegado.value.strip():
            delegado.error_text = "Campo requerido"
            valid = False
        else:
            delegado.error_text = None

        page.update()

        if not valid:
            return


        cargar_cursos_por_aula(selected_id)
        # si estamos en edición, intentar actualizar; si no, crear
        nonlocal edit_mode, editing_course_id
        if edit_mode:
            # intentar usar controlador actualizar_curso si está disponible
            if actualizar_curso:
                try:
                    # intento genérico; ajustar firma del controlador según tu implementación
                    actualizar_curso(editing_course_id, nombre_curso.value.strip(), docente.value.strip(), int(delegado.value.strip()))
                except Exception as ex:
                    print("Error al actualizar curso:", ex)
            else:
                print("Función actualizar_curso no implementada en controllers.")
        else:
            crear_curso(int(dropdown_aula.value), nombre_curso.value.strip(), docente.value.strip(), int(delegado.value.strip()))
        
        cargar_cursos_por_aula(selected_id)

        # cerrar modal y limpiar
        modal_container.visible = False
        nombre_curso.value = ""
        docente.value = ""
        delegado.value = ""
        page.update()


    # --- Funciones para abrir/cerrar el modal ---

    def abrir_modal(e):
        modal_container.visible = True
        page.update()

    def cerrar_modal(e):
        modal_container.visible = False
        # Opcional: limpiar campos al cerrar
        nombre_curso.value = ""
        docente.value = ""
        delegado.value = ""
        page.update()

        # resetear estado de edición y UI del modal
        nonlocal edit_mode, editing_course_id
        edit_mode = False
        editing_course_id = None
        try:
            modal_title.value = "CREAR CURSO"
        except Exception:
            pass
        try:
            btn_crear_modal.text = "CREAR"
        except Exception:
            pass
        page.update()

    # --- Botones del modal (Reutilizados y adaptados) ---
    btn_crear_modal = ft.ElevatedButton(
        text="CREAR",
        bgcolor="#2C2F3A",
        color=ft.Colors.WHITE,
        width=200,
        height=60,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        on_click=validar_y_crear_curso, # <-- Conectado a la nueva función
    )
    
    btn_cancelar_modal = ft.TextButton(
        text="Cancelar",
        on_click=cerrar_modal
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
                        modal_title,
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Divider(height=8, color=ft.Colors.TRANSPARENT),

                # Inputs (ocupando todo el ancho disponible del formulario)
                ft.Column(
                    [
                        ft.Container(content=nombre_curso, width=640),
                        ft.Container(content=docente, width=640),
                        ft.Container(content=delegado, width=640),
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

    # --- BOTÓN AÑADIR CURSO ---
    btn_add_curso = ft.ElevatedButton(
        text="Añadir Curso",
        icon=ft.Icons.ADD,
        bgcolor="#1F1F1F",
        color="#EAEAEA",
        height=45,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            side=ft.BorderSide(1, "#333333"),
            overlay_color=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
        ),
        on_click=abrir_modal,
    )



    # --- BOTÓN HOME ---
    btn_home = ft.IconButton(
        icon=ft.Icons.HOME,
        icon_size=30,
        icon_color=ft.Colors.WHITE,
        style=ft.ButtonStyle(
            bgcolor="#111111",
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
        on_click=lambda e: page.go("/options"),
    )


    # --- HEADER (TÍTULO + BOTONES DERECHA) ---
    titulo_header = ft.Text("Cursos", size=45, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)

    header = ft.Row(
        [
            titulo_header,
            ft.Container(expand=True),
            btn_add_curso,
            btn_home,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # --- CONTENIDO CENTRAL ---
    content = ft.Container(
        expand=True,
        padding=30,
        content=ft.Column(
            [
                header,
                ft.Container(height=30),
                cursos_grid,
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
    )

    # asignar el handler una vez que 'content' ya está creado
    dropdown_aula.on_change = on_aula_change

    # forzar carga inicial usando el value actual del dropdown (si existe)
    if list_aulas and dropdown_aula.value:
        class _E: pass
        e = _E()
        e.control = dropdown_aula
        on_aula_change(e)

    # --- ESTRUCTURA PRINCIPAL (SIDEBAR + CONTENIDO) ---
    layout = ft.Row(
        [
            sidebar,
            ft.VerticalDivider(width=1, color="#333333"),
            content,
        ],
        expand=True,
    )

    return ft.Container(
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[
                ft.Colors.BLACK,
                ft.Colors.with_opacity(0.97, ft.Colors.BLUE_GREY_900),
            ],
        ),
        content=ft.Stack(
            [
                # Elemento 1: El contenido principal (al fondo)
                layout,
                
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
