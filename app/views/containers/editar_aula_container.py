import flet as ft
from app.controllers.aulas_controller import actualizar_aula
from app.utils.vald_text_fields import validar_formulario
from app.controllers.aulas_usuario_controller import agregar_usuario_a_aula

def EditarAulaView(page: ft.Page, func_load_content, aula_dict: dict = None, on_update=None):
    """
    Vista moderna para editar un aula (igual al diseño mostrado en imagen).
    """

    # --- CONFIGURACIÓN DE PÁGINA ---
    page.title = "Aula 365 | Editar Aula"
    page.bgcolor = "#000000"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    # --- DATOS DEL AULA (si existen) ---
    nombre_val = aula_dict["nombre_aula"] if aula_dict else ""
    descripcion_val = aula_dict["descripcion"] if aula_dict else ""

    # --- TÍTULO PRINCIPAL ---
    titulo = ft.Text(
        "Editar Aula",
        size=40,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE,
    )

    # --- BOTÓN HOME ---
    btn_home = ft.IconButton(
        icon=ft.Icons.HOME,
        icon_color=ft.Colors.WHITE,
        icon_size=30,
        style=ft.ButtonStyle(
            shape=ft.CircleBorder(),
            bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
        ),
        tooltip="Volver al inicio",
        on_click=lambda e: page.go("/options"),
    )

    # --- CAMPOS DE TEXTO ---
    nombre_aula = ft.TextField(
        label="Nombre del Aula:",
        hint_text="Ejemplo: AULA 203",
        bgcolor="#2B2B2B",
        color=ft.Colors.WHITE,
        border_radius=10,
        width=400,
        value=nombre_val,
    )

    descripcion_aula = ft.TextField(
        label="Descripción del Aula:",
        hint_text="Ejemplo: AULA 203",
        bgcolor="#2B2B2B",
        color=ft.Colors.WHITE,
        border_radius=10,
        width=400,
        value=descripcion_val,
    )

    # --- BOTÓN CONFIRMAR ---
    def confirmar(e):
        # actualizar en BD
        actualizar_aula(
            id_aula=aula_dict["id_aula"],
            nombre_aula=nombre_aula.value,
            descripcion=descripcion_aula.value,
        )
        # snackbar y refresco local
        page.snack_bar = ft.SnackBar(ft.Text("✅ Aula actualizada correctamente"))
        page.snack_bar.open = True
        # notificar al dashboard (si se pasó callback)
        if callable(on_update):
            # actualizar el dict que se pasó (o reconstruir uno nuevo)
            aula_dict["nombre_aula"] = nombre_aula.value
            aula_dict["descripcion"] = descripcion_aula.value
            on_update(aula_dict)
        page.update()

    btn_confirmar = ft.ElevatedButton(
        text="Confirmar",
        bgcolor="#3A3A3A",
        color=ft.Colors.WHITE,
        width=180,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
        ),
        on_click=confirmar,
    )

    # --- LÍNEA DIVISORIA (hecha con un Container) ---
    linea_div = ft.Container(
        height=1,
        bgcolor="#666666",
        width=450,
        border_radius=1,
        opacity=0.7,
    )

    # --- BOTÓN GENERAR INVITACIÓN ---
    btn_invitacion = ft.ElevatedButton(
        text="Invitar Miembro",
        icon=ft.Icons.ADD,
        bgcolor="#3A3A3A",
        color=ft.Colors.WHITE,
        width=270,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        on_click=lambda e: (
            abrir_modal(e),
            setattr(page, "snack_bar", ft.SnackBar(ft.Text("📩 Invitación generada correctamente"))),
            setattr(page.snack_bar, "open", True),
            page.update(),
        ),
    )

    # --- BOTÓN VER MIEMBROS ---
    btn_miembros = ft.ElevatedButton(
        text="Ver Miembros",
        icon=ft.Icons.GROUP,
        bgcolor="#3A3A3A",
        color=ft.Colors.WHITE,
        width=270,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        on_click=lambda e: func_load_content("Miembros")
    )


    # ------------------------------------------------------
    # COMPONENTES DEL MODAL CREAR/EDITAR CURSO
    # ------------------------------------------------------
    id_usuario = ft.TextField(label="Ingresar ID: ", bgcolor="#1E1E1E", border_radius=10, border_color=ft.Colors.TRANSPARENT)
    modal_title = ft.Text("Agregar Miembro", weight=ft.FontWeight.BOLD, size=22, color=ft.Colors.WHITE)

    campos = [ id_usuario ]

    def validar_y_crear_curso(e):
        if not validar_formulario(page, campos):
            return
        
        try:
            agregar_usuario_a_aula(aula_dict["id_aula"], id_usuario.value, rol="ALUMNO")
            cerrar_modal(e)
        
        except Exception as ex:
            print(f"Error al guardar curso: {ex}")
            # Mostrar error en un SnackBar
            snack = ft.SnackBar(ft.Text(f"Error: {ex}"), bgcolor=ft.Colors.RED_700)
            page.overlay.append(snack)
            snack.open = True
            page.update()


    def abrir_modal(e):
        # Si no estamos editando, resetea los campos
        id_usuario.value = ""
        modal_title.value = "Agregar Miembro"
        btn_crear_modal.text = "Invitar"
        
        page.overlay.append(modal_container) # Usa overlay
        modal_container.visible = True
        page.update()

    def cerrar_modal(e):
        modal_container.visible = False
        page.overlay.remove(modal_container) # Usa overlay
        page.update()

    btn_crear_modal = ft.ElevatedButton(text="Invitar", on_click=validar_y_crear_curso)
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
                id_usuario,
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

    # --- ESTRUCTURA PRINCIPAL ---
    contenido = ft.Column(
        [
            ft.Row([titulo, ft.Container(expand=True), btn_home], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(height=30),
            nombre_aula,
            descripcion_aula,
            btn_confirmar,
            linea_div,
            btn_invitacion,
            btn_miembros,
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
    )

    # --- CONTAINER FINAL ---
    layout = ft.Container(
        expand=True,
        padding=ft.padding.all(50),
        content=contenido,
        alignment=ft.alignment.top_left,
    )

    return layout
