from typing import Optional
import flet as ft
from app.controllers.aulas_controller import obtener_aulas, obtener_aula_by_id
from app.controllers.cursos_controller import obtener_cursos
from app.views.containers.cursos_container import contenedor_cursos
from app.views.containers.curso_container import CursoDetalleView
from app.views.containers.tareas_container import TareasCursoView
from app.views.containers.editar_aula_container import EditarAulaView
from app.views.containers.miembros_container import MiembrosAulaView

# --- 1. Importar las nuevas "sub-vistas" ---

# ======================================================
#         VISTA PRINCIPAL (CONTENEDOR)
# ======================================================
def AulaDashboardView(page: ft.Page):
    # ------------------------------------------------------
    # 1️⃣ VALIDACIÓN DE SESIÓN
    # ------------------------------------------------------
    user = page.session.get("user")
    if not user:
        page.go("/login")
        return

    # Usar .get() es más seguro
    id_usuario = user.get("id_usuario") 
    nombre = user.get("nombre", "Usuario")
    apellido = user.get("apellido", "")


    # ------------------------------------------------------
    # 2️⃣ ESTADOS Y VARIABLES INTERNAS
    # ------------------------------------------------------
    # 'selected_id' ahora es la única variable de estado importante aquí
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

    # ---------- (A) Botón lateral ----------
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
            # Llama a la nueva función 'actualizar_contenido'
            on_click=lambda e: mostrar_contenido(text), 
        )

        container.on_hover = lambda e: (
            setattr(container, "bgcolor", hover_color if e.data == "true" else base_color),
            container.update()
        )
        return container

    # ------------------------------------------------------
    # 5️⃣ FUNCIONES LÓGICAS
    # ------------------------------------------------------

    def on_aula_change(e):
        nonlocal selected_id
        try:
            selected_id = int(e.control.value) if e.control and e.control.value is not None else None
        except Exception:
            selected_id = None
        print("DEBUG on_aula_change -> selected_id:", selected_id, type(selected_id))
        # carga automáticamente la vista de cursos para el aula seleccionada
        mostrar_contenido("Cursos")

    def actualizar_contenido(texto):
        # Carga la vista (Cursos o Anuncios) en el content_area
        
        id_aula_actual = selected_id.current
        if not id_aula_actual:
            content_area.content = ft.Container(
                content=ft.Text("Por favor, seleccione un aula.", color=ft.Colors.WHITE),
                alignment=ft.alignment.center,
                expand=True
            )
            page.update()
            return
            
        print(f"Cargando '{texto}' para el aula {id_aula_actual}")
        if texto == "Cursos":
            # Llama a la función CursosView y le pasa los datos
            content_area.content = contenedor_cursos(page, user, id_aula_actual)
        elif texto == "Anuncios":
            # Llama a la función AnunciosView
            content_area.content = contenedor_anuncios(page, user, id_aula_actual)

        page.update()

    def on_aula_updated(actualizada: dict):
        nonlocal list_aulas, dropdown_aula
        # recargar la lista desde BD (opcional) o actualizar el elemento en list_aulas
        try:
            list_aulas = obtener_aulas(id_usuario)
        except Exception:
            # fallback: actualizar el dict en memoria
            for i, a in enumerate(list_aulas):
                if a.get("id_aula") == actualizada.get("id_aula"):
                    list_aulas[i].update(actualizada)
                    break
        # reconstruir options usando ids como key
        dropdown_aula.options = [
            ft.dropdown.Option(key=str(a["id_aula"]), text=a["nombre_aula"]) for a in list_aulas
        ]
        # si el aula editada es la seleccionada, actualizar el value/text si quieres
        if str(actualizada.get("id_aula")) == dropdown_aula.value:
            # actualizar el value para forzar redraw (opcional)
            dropdown_aula.value = str(actualizada.get("id_aula"))
        page.update()

    def mostrar_contenido(view_name, curso_dict = None):
        # asegurar que selected_id es un int válido
        if not selected_id:
            content_area.content = ft.Container(
                content=ft.Text("Por favor, seleccione un aula.", color=ft.Colors.WHITE),
                alignment=ft.alignment.center,
                expand=True
            )
            page.update()
            return

        print("DEBUG mostrar_contenido -> selected_id:", selected_id, type(selected_id))

        # --- llamada segura al contenedor de cursos ---
        # Ajusta el orden según la firma de contenedor_cursos:
        #  - si su firma es contenedor_cursos(page, id_aula, user): usa la llamada siguiente
        # try:
        #     new_content = contenedor_cursos(page, selected_id, user)
        # except TypeError:
        #     # si la firma es distinta (page, user, id_aula) intenta con el orden inverso
        #     new_content = contenedor_cursos(page, user, selected_id)

        if view_name == "Cursos":
            new_content = contenedor_cursos(page, selected_id, mostrar_contenido)
        elif view_name == "Curso":
            new_content = CursoDetalleView(page, curso_dict, mostrar_contenido)
        elif view_name == "Anuncios":
            new_content = ft.Text("Anuncios (pendiente)", color=ft.Colors.WHITE)
        elif view_name == "Tareas":
            new_content = TareasCursoView(page, curso_dict, selected_id, mostrar_contenido)
        elif view_name == "Editar Aula":
            aula_dict = obtener_aula_by_id(selected_id)
            new_content = EditarAulaView(page, mostrar_contenido, aula_dict, on_update=on_aula_updated)
        elif view_name == "Miembros":
            new_content = MiembrosAulaView(page, selected_id)
        else:
            new_content = ft.Text("Inicio del curso", color=ft.Colors.WHITE)

        content_area.content = ft.Column([new_content])
        page.update()

    # ------------------------------------------------------
    # 6️⃣ SIDEBAR Y LAYOUT GENERAL
    # ------------------------------------------------------
    list_aulas = obtener_aulas(id_usuario) 
    
    dropdown_aula = ft.Dropdown(
        value=str(list_aulas[0]["id_aula"]) if list_aulas else None,
        options=[ft.dropdown.Option(key=str(a['id_aula']), text=a['nombre_aula']) for a in list_aulas],
        width=160,
        color=ft.Colors.WHITE,
        border_color="#333333",
        focused_border_color="#555555",
        on_change=on_aula_change,
    )

    user_info = ft.Column(
        [
            ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=70, color=ft.Colors.WHITE),
            ft.Text(f"{nombre} {apellido}", size=20, color=ft.Colors.LIGHT_BLUE_ACCENT, weight=ft.FontWeight.W_500),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5,
    )

    # (Tu código de btn_logout)
    btn_logout = ft.Container(
        content=ft.Text("Cerrar Sesión", color="#E0E0E0", size=16),
        width=160,
        height=45,
        alignment=ft.alignment.center,
        bgcolor="#201010",
        border_radius=8,
        border=ft.border.all(1, "#3A1A1A"),
        ink=True,
        on_click=lambda e: page.go("/login"), # <-- Deberías usar tu botón de utilidades
        on_hover=lambda e: (
            setattr(e.control, "bgcolor", "#2C1414" if e.data == "true" else "#201010"),
            e.control.update(),
        ),
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
                side_button("Editar Aula"),
                ft.Container(expand=True),
                btn_logout,
            ]
        ),
    )

    # ------------------------------------------------------
    # 7️⃣ CONTENIDO CENTRAL (AHORA ES UN CONTENEDOR VACÍO)
    # ------------------------------------------------------
    
    # Esta es el 'content' que el layout usará
    content_area = ft.Container(
        expand=True,
        padding=0, # El padding se manejará dentro de cada sub-vista
        alignment=ft.alignment.top_left,
        content=ft.Container(
            content=ft.Text("Cargando...", color=ft.Colors.WHITE),
            alignment=ft.alignment.center,
            expand=True
        )
    )

    # ------------------------------------------------------
    # CARGA INICIAL
    # ------------------------------------------------------
    if list_aulas:
        selected_id = list_aulas[0]["id_aula"]
        mostrar_contenido("Cursos") # Carga "Cursos" por defecto
    else:
        content_area.content = ft.Container(
            content=ft.Text("No estás inscrito en ninguna aula.", color=ft.Colors.WHITE),
            alignment=ft.alignment.center,
            expand=True
        )

    # ------------------------------------------------------
    # 9️⃣ ESTRUCTURA FINAL
    # ------------------------------------------------------
    layout = ft.Row(
        [
            sidebar, 
            ft.VerticalDivider(width=1, color="#333333"), 
            content_area # <--- Se usa el 'content_area' dinámico
        ], 
        expand=True
    )

    # El modal se ha movido a cursos_view, por lo que el Stack ya no es necesario aquí
    return ft.Container(
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.Colors.BLACK, ft.Colors.with_opacity(0.97, ft.Colors.BLUE_GREY_900)],
        ),
        content=layout, # Retorna solo el layout
        expand=True,
    )
    #"""