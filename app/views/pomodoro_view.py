import flet as ft
import asyncio

def PomodoroView(page: ft.Page):
    """
    Temporizador Pomodoro con estilo dark-petróleo medio.
    """
    # ================================
    # COLORES BASE
    # ================================
    COLOR_ACCENT = "#1C8DB0"
    COLOR_BG_CARD = "#141C22"
    COLOR_BG_HOVER = "#1D2A31"
    COLOR_TEXT = "#E8EAEA"
    COLOR_TEXT_SEC = "#AAB6B8"

    # ================================
    # CONFIGURACIÓN GENERAL
    # ================================
    page.title = "UniRed | Pomodoro"
    page.bgcolor = "#000000"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # --- ESTADOS INICIALES ---
    is_running = False
    is_break = False
    work_duration = 25 * 60
    break_duration = 5 * 60
    remaining_time = work_duration

    # ================================
    # COMPONENTES VISUALES
    # ================================
    estado_texto = ft.Text(
        "Tiempo de Enfoque",
        size=26,
        color=COLOR_TEXT,
        weight=ft.FontWeight.BOLD,
    )

    timer_text = ft.Text(
        "25:00",
        size=80,
        color=COLOR_TEXT,
        weight=ft.FontWeight.BOLD,
    )

    progress_ring = ft.ProgressRing(
        value=0,
        color=COLOR_ACCENT,
        width=220,
        height=220,
        stroke_width=10,
    )

    btn_home = ft.IconButton(
        icon=ft.Icons.HOME,
        icon_color=COLOR_TEXT,
        icon_size=28,
        tooltip="Volver al inicio",
        style=ft.ButtonStyle(
            shape=ft.CircleBorder(),
            bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
        ),
        on_click=lambda e: page.go("/options"),
    )

    # ================================
    # CAMPOS DE CONFIGURACIÓN
    # ================================
    tiempo_concentracion = ft.TextField(
        label="Tiempo de Enfoque (min)",
        value="25",
        width=180,
        bgcolor=COLOR_BG_CARD,
        color=COLOR_TEXT,
        border_radius=10,
        border_color="#2A3C44",
        focused_border_color=COLOR_ACCENT,
        label_style=ft.TextStyle(color=COLOR_TEXT_SEC),
    )

    tiempo_descanso = ft.TextField(
        label="Tiempo de Descanso (min)",
        value="5",
        width=180,
        bgcolor=COLOR_BG_CARD,
        color=COLOR_TEXT,
        border_radius=10,
        border_color="#2A3C44",
        focused_border_color=COLOR_ACCENT,
        label_style=ft.TextStyle(color=COLOR_TEXT_SEC),
    )

    # ================================
    # FUNCIONES AUXILIARES
    # ================================
    def format_time(seconds):
        mins, secs = divmod(seconds, 60)
        return f"{mins:02d}:{secs:02d}"

    def update_timer():
        timer_text.value = format_time(remaining_time)
        total = break_duration if is_break else work_duration
        progress_ring.value = 1 - (remaining_time / total)
        progress_ring.color = "#37E27E" if is_break else COLOR_ACCENT
        page.update()

    # ================================
    # LÓGICA PRINCIPAL DEL TEMPORIZADOR
    # ================================
    async def run_timer():
        nonlocal remaining_time, is_running, is_break
        while is_running and remaining_time > 0:
            await asyncio.sleep(1)
            remaining_time -= 1
            update_timer()

        if is_running:
            is_running = False
            if is_break:
                is_break = False
                remaining_time = work_duration
                estado_texto.value = "Tiempo de Enfoque"
                page.snack_bar = ft.SnackBar(ft.Text("🎯 ¡Vuelve al trabajo!"))
            else:
                is_break = True
                remaining_time = break_duration
                estado_texto.value = "Descanso ☕"
                page.snack_bar = ft.SnackBar(ft.Text("☕ Tómate un descanso"))
            page.snack_bar.open = True
            update_timer()

    # ================================
    # FUNCIONES DE CONTROL
    # ================================
    def start_timer(e):
        nonlocal is_running
        if not is_running:
            is_running = True
            page.run_task(run_timer)

    def pause_timer(e):
        nonlocal is_running
        is_running = False

    def reset_timer(e):
        nonlocal remaining_time, is_running, is_break
        is_running = False
        is_break = False
        remaining_time = work_duration
        estado_texto.value = "Tiempo de Enfoque"
        update_timer()

    def aplicar_config(e):
        nonlocal work_duration, break_duration, remaining_time, is_running, is_break
        try:
            work_duration = int(tiempo_concentracion.value) * 60
            break_duration = int(tiempo_descanso.value) * 60
            remaining_time = work_duration
            is_running = False
            is_break = False
            estado_texto.value = "Tiempo de Enfoque"
            update_timer()
            page.snack_bar = ft.SnackBar(ft.Text("Configuración actualizada ✅"))
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("⚠️ Introduce números válidos"))
        page.snack_bar.open = True
        page.update()

    # ================================
    # BOTONES
    # ================================
    def crear_boton(texto, color_bg, on_click):
        return ft.Container(
            content=ft.Text(texto, color=COLOR_TEXT, size=16, weight=ft.FontWeight.BOLD),
            bgcolor=color_bg,
            border_radius=10,
            width=120,
            height=50,
            alignment=ft.alignment.center,
            ink=True,
            on_click=on_click,
            animate=ft.Animation(200, "easeOut"),
            on_hover=lambda e: (
                setattr(
                    e.control,
                    "bgcolor",
                    ft.Colors.with_opacity(0.85, color_bg)
                    if e.data == "true"
                    else color_bg,
                ),
                e.control.update(),
            ),
        )

    btn_aplicar = crear_boton("Aplicar", COLOR_ACCENT, aplicar_config)
    btn_iniciar = crear_boton("Iniciar", COLOR_ACCENT, start_timer)
    btn_pausar = crear_boton("Pausar", "#FF8C00", pause_timer)
    btn_reiniciar = crear_boton("Reiniciar", "#B22222", reset_timer)

    configuracion = ft.Row(
        [tiempo_concentracion, tiempo_descanso, btn_aplicar],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15,
    )

    botones_row = ft.Row(
        [btn_iniciar, btn_pausar, btn_reiniciar],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=25,
    )

    # ================================
    # ESTRUCTURA VISUAL
    # ================================
    header = ft.Row(
        [ft.Container(expand=True), btn_home],
        alignment=ft.MainAxisAlignment.END,
    )

    content = ft.Column(
        [
            header,
            ft.Container(height=40),
            ft.Text(
                "Pomodoro",
                size=42,
                weight=ft.FontWeight.BOLD,
                color=COLOR_TEXT,
            ),
            ft.Container(height=15),
            configuracion,
            ft.Container(height=40),
            estado_texto,
            ft.Container(
                ft.Stack(
                    [
                        progress_ring,
                        ft.Container(timer_text, alignment=ft.alignment.center),
                    ],
                    alignment=ft.alignment.center,
                ),
                alignment=ft.alignment.center,
                width=300,
                height=220,
            ),
            ft.Container(height=30),
            botones_row,
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    layout = ft.Container(
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#0A161B", "#0E2329", "#08171C"],
        ),
        expand=True,
        padding=ft.padding.all(40),
        content=content,
    )

    update_timer()
    return layout
