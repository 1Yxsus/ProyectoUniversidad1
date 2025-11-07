import flet as ft
from app.controllers.aulas_controller import obtener_aulas
from app.controllers.cursos_controller import crear_curso, obtener_cursos, actualizar_curso
from app.views.containers.curso_container import CursoDetalleView
from app.utils.vald_text_fields import validar_formulario


# ======================================================
#                     VISTA PRINCIPAL
# ======================================================
def AulaDashboardView(page: ft.Page):
    # ------------------------------------------------------
    # 1️⃣ VALIDACIÓN DE SESIÓN
    # ------------------------------------------------------
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
    # 2️⃣ ESTADOS Y VARIABLES INTERNAS
    # ------------------------------------------------------
    edit_mode = False
    editing_course_id = None
    selected_id = None

    # ------------------------------------------------------
    # 3️⃣ CONFIGURACIÓN DE PÁGINA
    # ------------------------------------------------------
    page.bgcolor = "#000000"
    page.title = "UniRed - Aula Dashboard"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # ------------------------------------------------------
    # 4️⃣ COMPONENTES DE INTERFAZ REUTILIZABLES
    # ------------------------------------------------------

    # ---------- (A) Tarjeta de Curso ----------
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
                                tooltip="Editar curso",
                                on_click=lambda e, c=curso_dict: abrir_modal_para_editar(c),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Text(f"Docente: {docente}", color="#A8A8A8", size=14),
                    ft.Text(f"Delegado: {delegado}", color="#A8A8A8", size=14),
                ],
                spacing=6,
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
            on_click=lambda e, c=curso_dict: cargar_curso_container(c),
        )

    # ---------- (B) Grid de Cursos ----------
    def course_grid(cards, max_per_row=3):
        rows = []
        for i in range(0, len(cards), max_per_row):
            rows.append(ft.Row(cards[i:i + max_per_row], spacing=20))
        return ft.Container(content=ft.Column(rows, spacing=20))

    # ---------- (C) Botón lateral ----------
    def side_button(text):
        base_color = "#1A1A1A"
        hover_color = "#2A2A2A"
        text_color = "#E0E0E0"

        container = ft.Container(
            content=ft.Text(text, color=text_color, size=17),
            width=160,
            height=45,
            alignment=ft.alignment.center,
            bgcolor=base_color,
            border_radius=8,
            border=ft.border.all(1, "#2E2E2E"),
            ink=True,
            on_click=lambda e: actualizar_contenido(text),
        )

        container.on_hover = lambda e: (
            setattr(container, "bgcolor", hover_color if e.data == "true" else base_color),
            container.update()
        )
        return container

    # ------------------------------------------------------
    # 5️⃣ FUNCIONES LÓGICAS
    # ------------------------------------------------------
    def abrir_modal_para_editar(curso_dict):
        nonlocal edit_mode, editing_course_id
        editing_course_id = curso_dict.get("id_curso")
        nombre_curso.value = curso_dict.get("curso")
        docente.value = curso_dict.get("docente") or ""
        delegado.value = str(curso_dict.get("id_delegado") or "")

        edit_mode = True
        modal_title.value = "EDITAR CURSO"
        btn_crear_modal.text = "GUARDAR"
        modal_container.visible = True
        page.update()

    def cargar_cursos_por_aula(id_aula):
        cursos_list = obtener_cursos(id_aula)
        cards = [course_card(c) for c in cursos_list]
        cursos_grid = course_grid(cards, max_per_row=4)
        content.content.controls[2] = cursos_grid
        page.update()

    def on_aula_change(e):
        nonlocal selected_id
        selected_id = int(e.control.value) if e.control.value else None
        cargar_cursos_por_aula(selected_id)

    def actualizar_titulo(texto):
        titulo_header.value = texto
        page.update()

    def actualizar_contenido(texto):
        actualizar_titulo(texto)
        if texto == "Cursos":
            cargar_cursos_por_aula(selected_id)
        elif texto == "Anuncios":
            content.content.controls[2] = ft.Text("Sección de Anuncios en construcción...", color=ft.Colors.WHITE)
        page.update()

    def cargar_curso_container(curso_dict):
        curso_vista = CursoDetalleView(page, curso_dict, selected_id, cargar_cursos_por_aula)
        content.content.controls[2] = curso_vista
        page.update()

    # ------------------------------------------------------
    # 6️⃣ COMPONENTES DEL MODAL CREAR/EDITAR CURSO
    # ------------------------------------------------------
    nombre_curso = ft.TextField(label="Nombre del Curso:", bgcolor="#1E1E1E", border_radius=10)
    docente = ft.TextField(label="Docente:", bgcolor="#1E1E1E", border_radius=10)
    delegado = ft.TextField(label="Delegado:", bgcolor="#1E1E1E", border_radius=10)
    modal_title = ft.Text("CREAR CURSO", weight=ft.FontWeight.BOLD, size=22, color=ft.Colors.WHITE)

    campos = [nombre_curso, docente, delegado]

    # Lógica para guardar
    print("Datos correctos ✅")

    def validar_y_crear_curso(e):
        nonlocal edit_mode, editing_course_id
        if not validar_formulario(page, campos):
            return
        if edit_mode:
            actualizar_curso(editing_course_id, nombre_curso.value, docente.value, int(delegado.value))
        else:
            crear_curso(int(dropdown_aula.value), nombre_curso.value, docente.value, int(delegado.value))
        cerrar_modal(e)
        cargar_cursos_por_aula(selected_id)

    def abrir_modal(e):
        modal_container.visible = True
        page.update()

    def cerrar_modal(e):
        nonlocal edit_mode, editing_course_id
        modal_container.visible = False
        nombre_curso.value = docente.value = delegado.value = ""
        edit_mode = False
        editing_course_id = None
        modal_title.value = "CREAR CURSO"
        btn_crear_modal.text = "CREAR"
        page.update()

    btn_crear_modal = ft.ElevatedButton(text="CREAR", on_click=validar_y_crear_curso)
    btn_cancelar_modal = ft.TextButton(text="Cancelar", on_click=cerrar_modal)

    form_container = ft.Container(
        width=700,
        height=400,
        bgcolor="#121212",
        border_radius=12,
        padding=30,
        content=ft.Column(
            [
                ft.Row([ft.Icon(ft.Icons.ADD_BOX_OUTLINED), modal_title], spacing=10),
                nombre_curso, docente, delegado,
                ft.Row([btn_cancelar_modal, btn_crear_modal], alignment=ft.MainAxisAlignment.END),
            ],
            spacing=10,
        ),
    )

    modal_container = ft.Container(
        bgcolor=ft.Colors.with_opacity(0.6, ft.Colors.BLACK),
        expand=True,
        alignment=ft.alignment.center,
        content=form_container,
        visible=False,
    )

    # ------------------------------------------------------
    # 7️⃣ SIDEBAR Y LAYOUT GENERAL
    # ------------------------------------------------------
    list_aulas = obtener_aulas(id)
    dropdown_aula = ft.Dropdown(
        value=str(list_aulas[0]["id_aula"]) if list_aulas else None,
        options=[ft.dropdown.Option(key=str(a['id_aula']), text=a['nombre_aula']) for a in list_aulas],
        width=150,
        on_change=on_aula_change,
    )

    user_info = ft.Column(
        [
            ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=70, color=ft.Colors.WHITE),
            ft.Text(f"{nombre} {apellido}", size=20, color=ft.Colors.LIGHT_BLUE_ACCENT),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

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
                side_button("Cursos"),
                side_button("Anuncios"),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Text("Cerrar Sesión", color="#E0E0E0"),
                    on_click=lambda e: page.go("/login"),
                ),
            ]
        ),
    )

    # ------------------------------------------------------
    # 8️⃣ CONTENIDO CENTRAL Y HEADER
    # ------------------------------------------------------
    btn_add_curso = ft.ElevatedButton(text="Añadir Curso", icon=ft.Icons.ADD, on_click=abrir_modal)
    btn_home = ft.IconButton(icon=ft.Icons.HOME, on_click=lambda e: page.go("/options"))
    titulo_header = ft.Text("Cursos", size=45, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)

    header = ft.Row(
        [titulo_header, ft.Container(expand=True), btn_add_curso, btn_home],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    cursos_grid = course_grid([], max_per_row=4)

    content = ft.Container(
        expand=True,
        padding=30,
        content=ft.Column([header, ft.Container(height=30), cursos_grid]),
    )

    # ------------------------------------------------------
    # MOSTRAR CURSOS DEL PRIMER AULA AUTOMÁTICAMENTE
    # ------------------------------------------------------
    if list_aulas:
        selected_id = list_aulas[0]["id_aula"]
        cargar_cursos_por_aula(selected_id)

    # ------------------------------------------------------
    # 9️⃣ ESTRUCTURA FINAL
    # ------------------------------------------------------
    layout = ft.Row([sidebar, ft.VerticalDivider(width=1, color="#333333"), content], expand=True)

    return ft.Container(
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.Colors.BLACK, ft.Colors.with_opacity(0.97, ft.Colors.BLUE_GREY_900)],
        ),
        content=ft.Stack([layout, modal_container], expand=True),
        expand=True,
    )
