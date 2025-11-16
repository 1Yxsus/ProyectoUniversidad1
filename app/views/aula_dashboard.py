from typing import Optional
import flet as ft
from app.controllers.aulas_controller import obtener_aulas, obtener_aula_by_id
from app.controllers.cursos_controller import obtener_cursos
from app.views.containers.cursos_container import contenedor_cursos
from app.views.containers.curso_container import CursoDetalleView
from app.views.containers.tareas_container import TareasCursoView
from app.views.containers.editar_aula_container import EditarAulaView
from app.views.containers.miembros_container import MiembrosAulaView
from app.controllers.aulas_usuario_controller import obtener_roles_por_usuario
from app.views.containers.silabus_container import SyllabusCursoView
from app.views.containers.anuncios_container import AnunciosAulaView
from app.views.containers.perfil_container import PerfilUsuarioView

def AulaDashboardView(page: ft.Page):
    # ------------------------------------------------------
    # VALIDACIÓN DE SESIÓN
    # ------------------------------------------------------
    user = page.session.get("user")
    if not user:
        page.go("/login")
        return

    id_usuario = user.get("id_usuario")
    nombre = user.get("nombre", "Usuario")
    apellido = user.get("apellido", "")
    roles_by_aula = page.session.get("roles_by_aula")

    selected_id = None
    current_actualizar_titulo = None

    sidebar_name_text = ft.Text(nombre,
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color="#FFFFFF",
                    text_align=ft.TextAlign.CENTER,)
    
    sidebar_apellido_text = ft.Text(
                    apellido,
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color="#FFFFFF",
                    text_align=ft.TextAlign.CENTER,)

    # ------------------------------------------------------
    # CONFIGURACIÓN DE PÁGINA
    # ------------------------------------------------------
    page.title = "UniRed | Dashboard de Aula"
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    # ------------------------------------------------------
    # BOTÓN LATERAL (TONO DARK MODERNO)
    # ------------------------------------------------------
    def side_button(text):
        base_color = "#141A1F"
        hover_color = "#1C242B"
        text_color = "#E8E8E8"

        btn = ft.Container(
            content=ft.Text(text, color=text_color, size=16, weight=ft.FontWeight.W_400),
            width=170,
            height=45,
            bgcolor=base_color,
            alignment=ft.alignment.center,
            border_radius=10,
            border=ft.border.all(1, "#222A30"),
            ink=True,
            on_click=lambda e: mostrar_contenido(text),
        )

        btn.on_hover = lambda e: (
            setattr(btn, "bgcolor", hover_color if e.data == "true" else base_color),
            btn.update(),
        )
        return btn

    # ------------------------------------------------------
    # FUNCIÓN: CAMBIO DE CONTENIDO
    # ------------------------------------------------------
    def mostrar_contenido(view_name, curso_dict=None):
        nonlocal current_actualizar_titulo
        if not selected_id:
            content_area.content = ft.Container(
                content=ft.Text("Por favor, selecciona un aula.", color="#CCCCCC", size=16),
                alignment=ft.alignment.center,
                expand=True,
            )
            page.update()
            return

        id_aula_int = int(selected_id)
        role = roles_by_aula.get(id_aula_int) if roles_by_aula else None

        if view_name == "Cursos":
            res = contenedor_cursos(page, selected_id, mostrar_contenido)
            if isinstance(res, tuple) and len(res) == 2:
                new_content, current_actualizar_titulo = res
            else:
                new_content = res
        elif view_name == "Curso":
            new_content = CursoDetalleView(page, curso_dict, mostrar_contenido)
        elif view_name == "Notificaciones":
            new_content = AnunciosAulaView(page, selected_id)
        elif view_name == "Tareas":
            new_content = TareasCursoView(page, curso_dict, selected_id, mostrar_contenido)
        elif view_name == "Editar Aula":
            aula_dict = obtener_aula_by_id(selected_id)
            if callable(current_actualizar_titulo):
                new_content = EditarAulaView(page, mostrar_contenido, aula_dict, on_update=current_actualizar_titulo)
            else:
                new_content = EditarAulaView(page, mostrar_contenido, aula_dict)
        elif view_name == "Miembros":
            new_content = MiembrosAulaView(page, mostrar_contenido, selected_id)
        elif view_name == "Silabus":
            new_content = SyllabusCursoView(page, curso_dict, selected_id, mostrar_contenido)
        elif view_name == "Perfil":
            def on_user_update(u):
                try:
                    sidebar_name_text.value = f"{u.get('nombre','')}"
                    sidebar_apellido_text.value = f"{u.get('apellido','')}"
                    page.update()
                except Exception:
                    pass

            new_content = PerfilUsuarioView(page, id_usuario, on_user_update=on_user_update)
        else:
            new_content = ft.Container(
                content=ft.Text(f"Vista '{view_name}' en desarrollo", color="#AAAAAA"),
                alignment=ft.alignment.center,
            )

        content_area.content = ft.Container(content=new_content, expand=True)
        page.update()

    # ------------------------------------------------------
    # SIDEBAR (CON GRADIENTE OSCURO SUAVE)
    # ------------------------------------------------------
    list_aulas = obtener_aulas(id_usuario)

    user_info = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Icon(
                        ft.Icons.ACCOUNT_CIRCLE,
                        size=90,
                        color="#DDE2E4",
                    ),
                    alignment=ft.alignment.center,
                ),
                sidebar_name_text,
                sidebar_apellido_text,
                ft.Text(
                    "Usuario Activo",
                    size=13,
                    color="#A0A6A8",
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6,
        ),
        padding=20,
        border_radius=12,
        bgcolor="#10171C",
        border=ft.border.all(1, "#1F2A32"),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=6,
            color=ft.Colors.with_opacity(0.15, "#000000"),
            offset=ft.Offset(0, 3),
        ),
    )

    btn_logout = ft.Container(
        content=ft.Text("Cerrar sesión", color="#EAEAEA", size=15),
        width=170,
        height=45,
        bgcolor="#162020",
        border_radius=10,
        border=ft.border.all(1, "#2C2C2C"),
        alignment=ft.alignment.center,
        ink=True,
        on_click=lambda e: page.go("/login"),
        on_hover=lambda e: (
            setattr(e.control, "bgcolor", "#1F2A2A" if e.data == "true" else "#162020"),
            e.control.update(),
        ),
    )

    sidebar = ft.Container(
        width=220,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#0C141A", "#0F1C23", "#0C181D"],
        ),
        padding=20,
        border=ft.border.only(right=ft.border.BorderSide(1, "#1E252B")),
        content=ft.Column(
            [
                user_info,
                ft.Container(height=25),
                side_button("Cursos"),
                side_button("Notificaciones"),
                side_button("Editar Aula"),
                ft.Container(expand=True),
                side_button("Perfil"),
                btn_logout,
            ],
            spacing=12,
        ),
    )

    # ------------------------------------------------------
    # CONTENIDO CENTRAL
    # ------------------------------------------------------
    content_area = ft.Container(
        expand=True,
        padding=0,
        alignment=ft.alignment.top_left,
        content=ft.Container(
            content=ft.Text("Cargando...", color="#AAAAAA", size=16),
            alignment=ft.alignment.center,
            expand=True,
        ),
    )

    # ------------------------------------------------------
    # CARGA INICIAL
    # ------------------------------------------------------
    session_selected_id = page.session.get("selected_aula_id")
    try:
        session_selected_id = int(session_selected_id) if session_selected_id else None
    except Exception:
        session_selected_id = None

    if list_aulas:
        selected_id = session_selected_id or list_aulas[0].get("id_aula")
        mostrar_contenido("Cursos")
    else:
        content_area.content = ft.Container(
            content=ft.Text("No estás inscrito en ninguna aula.", color="#AAAAAA", size=16),
            alignment=ft.alignment.center,
            expand=True,
        )

    # ------------------------------------------------------
    # DISEÑO FINAL (GRADIENTE COMPATIBLE CON TODAS LAS VISTAS)
    # ------------------------------------------------------
    layout = ft.Row(
        [sidebar, ft.VerticalDivider(width=1, color="#2B2B2B"), content_area],
        expand=True,
    )

    # Fondo dark con matices azul-verde, combinando con “Anuncios” y “Cursos”
    background = ft.Stack(
        [
            ft.Container(
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=[
                        "#0C1C24",  # azul petróleo oscuro
                        "#0E2329",  # tono intermedio
                        "#08171C",  # casi negro, con reflejo verde-azul
                    ],
                ),
                expand=True,
            ),
            ft.Container(
                bgcolor=ft.Colors.with_opacity(0.04, "#FFFFFF"),
                expand=True,
            ),
            layout,
        ],
        expand=True,
    )

    return background
