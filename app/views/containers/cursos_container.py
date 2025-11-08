import flet as ft
from app.controllers.cursos_controller import crear_curso, obtener_cursos, actualizar_curso
from app.utils.vald_text_fields import validar_formulario

# ======================================================
#             VISTA DE CURSOS (CONTENIDO)
# ======================================================
def contenedor_cursos(page: ft.Page, user: dict, id_aula: int):
    
    # ------------------------------------------------------
    # ESTADOS Y VARIABLES
    # ------------------------------------------------------
    edit_mode = False
    editing_course_id = None
    
    view_content = ft.Ref[ft.Container]() # Sigue siendo útil si quieres cambiar vistas internas

    # ------------------------------------------------------
    # FUNCIONES LÓGICAS
    # ------------------------------------------------------

    def cargar_grid_cursos(id_aula_cargada):
        """ Carga el grid de cursos en el 'view_content' """
        cursos_list = obtener_cursos(id_aula_cargada)
        cards = [course_card(c) for c in cursos_list]
        
        if not cards:
            grid = ft.Container(
                content=ft.Text("No hay cursos creados en esta aula.", color=ft.Colors.WHITE),
                alignment=ft.alignment.center,
                expand=True
            )
        else:
            grid = course_grid(cards, max_per_row=4)
        
        # Actualiza el contenido del contenedor principal
        if view_content.current:
            view_content.current.content = ft.Column(
                [header, ft.Container(height=30), grid],
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True
            )
            page.update()

    # --- FUNCIÓN ELIMINADA ---
    # Ya no usamos 'cargar_curso_container'
    # def cargar_curso_container(curso_dict):
    #     ...

    # ------------------------------------------------------
    # COMPONENTES DE INTERFAZ
    # ------------------------------------------------------

    # ---------- (A) Tarjeta de Curso ----------
    def course_card(curso_dict):
        nombre = curso_dict.get("curso")
        docente = curso_dict.get("docente")
        delegado = curso_dict.get("delegado")
        curso_id = curso_dict.get("id_curso") # Obtenemos el ID del curso

        def abrir_tareas_curso(e):
            """Navega a la vista de tareas del curso específico"""
            print(f"Navegando a /curso/{curso_id}/tareas")
            page.go(f"/curso/{curso_id}/tareas")

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
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            on_hover=lambda e: (
                setattr(e.control, "bgcolor", "#1E1E1E" if e.data == "true" else "#151515"),
                e.control.update(),
            ),
            # --- ON_CLICK CORREGIDO ---
            # Al hacer clic, llama a la función de navegación
            on_click=abrir_tareas_curso,
        )

    # ---------- (B) Grid de Cursos ----------
    def course_grid(cards, max_per_row=3):
        rows = []
        for i in range(0, len(cards), max_per_row):
            rows.append(ft.Row(cards[i:i + max_per_row], spacing=20))
        return ft.Container(content=ft.Column(rows, spacing=20))

    # ------------------------------------------------------
    # COMPONENTES DEL MODAL CREAR/EDITAR CURSO
    # ------------------------------------------------------
    nombre_curso = ft.TextField(label="Nombre del Curso:", bgcolor="#1E1E1E", border_radius=10, border_color=ft.Colors.TRANSPARENT)
    docente = ft.TextField(label="Docente:", bgcolor="#1E1E1E", border_radius=10, border_color=ft.Colors.TRANSPARENT)
    delegado = ft.TextField(label="Delegado:", bgcolor="#1E1E1E", border_radius=10, border_color=ft.Colors.TRANSPARENT)
    modal_title = ft.Text("CREAR CURSO", weight=ft.FontWeight.BOLD, size=22, color=ft.Colors.WHITE)
    campos = [nombre_curso, docente, delegado]

    def validar_y_crear_curso(e):
        nonlocal edit_mode, editing_course_id
        if not validar_formulario(page, campos):
            return
        
        try:
            if edit_mode:
                actualizar_curso(editing_course_id, nombre_curso.value, docente.value, int(delegado.value))
            else:
                crear_curso(id_aula, nombre_curso.value, docente.value, int(delegado.value))
            
            cerrar_modal(e)
            cargar_grid_cursos(id_aula) # Recarga el grid
        
        except Exception as ex:
            print(f"Error al guardar curso: {ex}")
            # Mostrar error en un SnackBar
            snack = ft.SnackBar(ft.Text(f"Error: {ex}"), bgcolor=ft.Colors.RED_700)
            page.overlay.append(snack)
            snack.open = True
            page.update()


    def abrir_modal_para_editar(curso_dict):
        nonlocal edit_mode, editing_course_id
        editing_course_id = curso_dict.get("id_curso")
        nombre_curso.value = curso_dict.get("curso")
        docente.value = curso_dict.get("docente") or ""
        delegado.value = str(curso_dict.get("id_delegado") or "")
        edit_mode = True
        modal_title.value = "EDITAR CURSO"
        btn_crear_modal.text = "GUARDAR"
        abrir_modal(e=None) # Llama a la función de abrir modal

    def abrir_modal(e):
        # Si no estamos editando, resetea los campos
        if not edit_mode:
            nombre_curso.value = ""
            docente.value = ""
            delegado.value = ""
            modal_title.value = "CREAR CURSO"
            btn_crear_modal.text = "CREAR"
        
        page.overlay.append(modal_container) # Usa overlay
        modal_container.visible = True
        page.update()

    def cerrar_modal(e):
        nonlocal edit_mode, editing_course_id
        modal_container.visible = False
        page.overlay.remove(modal_container) # Usa overlay
        edit_mode = False
        editing_course_id = None
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
    # HEADER (Botones Añadir Curso y Home)
    # ------------------------------------------------------
    btn_add_curso = ft.ElevatedButton(text="Añadir Curso", icon=ft.Icons.ADD, on_click=abrir_modal, bgcolor="#1F1F1F", color="#EAEAEA")
    btn_home = ft.IconButton(icon=ft.Icons.HOME, on_click=lambda e: page.go("/options"), icon_color=ft.Colors.WHITE, bgcolor="#111111")

    titulo_header = ft.Text("Cursos", size=45, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)

    header = ft.Row(
        [titulo_header, ft.Container(expand=True), btn_add_curso, btn_home],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # ------------------------------------------------------
    # CONTENIDO INICIAL DE LA VISTA
    # ------------------------------------------------------
    cursos_list_inicial = obtener_cursos(id_aula)
    cards_iniciales = [course_card(c) for c in cursos_list_inicial]
    if not cards_iniciales:
        grid_inicial = ft.Container(
            content=ft.Text("No hay cursos creados en esta aula.", color=ft.Colors.WHITE),
            alignment=ft.alignment.center,
            expand=True
        )
    else:
        grid_inicial = course_grid(cards_iniciales, max_per_row=4)

    # ------------------------------------------------------
    # ESTRUCTURA FINAL DE LA VISTA
    # ------------------------------------------------------
    
    # Este es el contenido principal de la vista de cursos
    main_cursos_content = ft.Column(
        [header, ft.Container(height=30), grid_inicial],
        scroll=ft.ScrollMode.ADAPTIVE,
        expand=True
    )

    # El 'view_content' (Ref) apunta a este contenedor
    # para que 'cargar_curso_container' pueda reemplazarlo
    view_wrapper = ft.Container(
        ref=view_content,
        content=main_cursos_content,
        expand=True,
        padding=30
    )

    # Retorna un Stack para que el modal funcione
    return ft.Stack(
        [
            view_wrapper,
            modal_container
        ],
        expand=True
    )


"""

import flet as ft
from app.views.containers.tareas_container import TareasCursoView

def CursoDetalleView(page: ft.Page, curso_dict: dict, selected_id: int, func_cursos_load):

    # Retorna la vista de detalle de un curso específico.
    # Muestra el nombre del curso y opciones: TAREAS y SILABUS.

    # --- FUNCIONES INTERNAS ---
    
    def cargar_tareas():
        tareas_vista = TareasCursoView(page, curso_dict, selected_id, func_cursos_load)
        layout.content = tareas_vista
        page.update()


    # --- DATOS DEL CURSO ---
    curso_nombre = curso_dict.get("curso")

    # --- TÍTULO DEL CURSO ---
    titulo_curso = ft.Text(
        curso_nombre,
        size=40,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE,
    )

    # --- BOTÓN VOLVER ---
    btn_volver = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        icon_color=ft.Colors.WHITE,
        icon_size=26,
        style=ft.ButtonStyle(
            shape=ft.CircleBorder(),
            bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
        ),
        tooltip="Volver",
        on_click=lambda e: func_cursos_load(selected_id),
    )

    # --- HEADER SUPERIOR ---
    header = ft.Row(
        [
            titulo_curso,
            ft.Container(expand=True),
            btn_volver,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # --- FUNCIÓN PARA BOTONES DE MÓDULO ---
    def boton_modulo(icono, texto, func_load_content):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Text(
                        texto,
                        size=20,
                        color=ft.Colors.WHITE,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Icon(icono, color=ft.Colors.WHITE, size=35),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            width=480,
            height=90,
            bgcolor="#151515",
            border_radius=12,
            border=ft.border.all(1, "#2A2A2A"),
            padding=ft.padding.symmetric(horizontal=25, vertical=15),
            ink=True,
            animate=ft.Animation(150,ft.AnimationCurve.EASE_IN_OUT),
            on_hover=lambda e: (
                setattr(e.control, "bgcolor", "#1E1E1E" if e.data == "true" else "#151515"),
                e.control.update(),
            ),
            on_click= lambda e: func_load_content(),
        )

    # --- BOTONES DE OPCIONES ---
    btn_tareas = boton_modulo(ft.Icons.CHECKLIST_ROUNDED, "TAREAS", cargar_tareas)
    btn_silabus = boton_modulo(ft.Icons.DESCRIPTION_ROUNDED, "SILABUS", cargar_tareas)

    # --- ESTRUCTURA PRINCIPAL ---
    contenido = ft.Column(
        [
            header,
            ft.Container(height=50),
            btn_tareas,
            btn_silabus,
        ],
        spacing=25,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # --- CONTAINER FINAL ---
    layout = ft.Container(
        content=contenido,
        alignment=ft.alignment.top_center,
        expand=True,
        padding=ft.padding.all(40),
        bgcolor="#000000",
    )

    return layout


"""