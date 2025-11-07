import flet as ft
from app.views.containers.tareas_container import TareasCursoView

def CursoDetalleView(page: ft.Page, curso_dict: dict, selected_id: int, func_cursos_load):
    """
    Retorna la vista de detalle de un curso específico.
    Muestra el nombre del curso y opciones: TAREAS y SILABUS.
    """
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
            animate=ft.Animation(150, "easeOut"),
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
