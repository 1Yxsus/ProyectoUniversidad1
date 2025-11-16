import flet as ft
import threading

# Mantiene referencia para evitar duplicados
_current_toast = None


def show_success(page: ft.Page, message: str = "Operación exitosa"):
    """Muestra un toast animado abajo-derecha, elegante y reutilizable."""

    global _current_toast

    # Si ya hay un toast, lo removemos
    try:
        if _current_toast and _current_toast in page.overlay:
            page.overlay.remove(_current_toast)
    except:
        pass

    # -------------------------------
    # Caja del toast
    # -------------------------------
    toast_box = ft.Container(
        padding=16,
        border_radius=12,
        bgcolor="#14A44D",
        shadow=ft.BoxShadow(
            blur_radius=18,
            color=ft.Colors.with_opacity(0.25, "#000000"),
            offset=ft.Offset(0, 4),
        ),
        content=ft.Row(
            [
                ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color="white", size=28),
                ft.Text(
                    message,
                    size=16,
                    color="white",
                    weight=ft.FontWeight.BOLD,
                ),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
        ),
    )

    # -------------------------------
    # Overlay positionado abajo-derecha
    # -------------------------------
    _current_toast = ft.Container(
        content=toast_box,
        right=20,
        bottom=20,
        animate_position=ft.Animation(400, "easeOut"),
        animate_opacity=ft.Animation(400, "easeOut"),
        opacity=0,
    )

    page.overlay.append(_current_toast)
    page.update()

    # -------------------------------
    # Animación de entrada
    # -------------------------------
    _current_toast.opacity = 1
    _current_toast.right = 20
    _current_toast.bottom = 20
    page.update()

    # -------------------------------
    # Autoremove con animación de salida
    # -------------------------------
    def _hide():
        try:
            if _current_toast in page.overlay:
                _current_toast.opacity = 0
                _current_toast.bottom = -30  # sube un poco para animación
                page.update()
                threading.Timer(0.35, lambda: page.overlay.remove(_current_toast)).start()
        except:
            pass

    threading.Timer(1.7, _hide).start()
