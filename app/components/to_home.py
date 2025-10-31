import flet as ft

def BotonHome(on_click=None):
    btn_home = ft.IconButton(
        icon=ft.Icons.HOME,
        icon_color=ft.Colors.WHITE,
        bgcolor=ft.Colors.GREY_900,
        tooltip="Ir al inicio",
        on_click=on_click,  # usa el callback recibido
    )

    btn_home_container = ft.Container(
        content=btn_home,
        alignment=ft.alignment.top_right,
    )

    return btn_home_container
