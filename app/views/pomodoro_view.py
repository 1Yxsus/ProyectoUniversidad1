import flet as ft
import asyncio

def PomodoroView(page: ft.Page):
    page.title = "Aula 365 | Pomodoro"
    page.bgcolor = "#000000"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # --- ESTADOS INICIALES ---
    is_running = False
    is_break = False
    work_duration = 25 * 60   # 25 minutos
    break_duration = 5 * 60   # 5 minutos
    remaining_time = work_duration

    # --- COMPONENTES VISUALES ---
    estado_texto = ft.Text("Tiempo de Enfoque", size=25, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
    timer_text = ft.Text("25:00", size=80, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
    progress_ring = ft.ProgressRing(value=0, color=ft.Colors.LIGHT_BLUE_ACCENT, width=200, height=200)

    btn_home = ft.IconButton(
        icon=ft.Icons.HOME,
        icon_color=ft.Colors.WHITE,
        icon_size=30,
        bgcolor="#111111",
        on_click=lambda e: page.go("/options")
    )

    # --- CAMPOS DE CONFIGURACIÓN ---
    tiempo_concentracion = ft.TextField(
        label="Tiempo de Enfoque (min)",
        value="25",
        width=180,
        bgcolor="#1A1A1A",
        color=ft.Colors.WHITE,
        border_radius=10,
    )

    tiempo_descanso = ft.TextField(
        label="Tiempo de Descanso (min)",
        value="5",
        width=180,
        bgcolor="#1A1A1A",
        color=ft.Colors.WHITE,
        border_radius=10,
    )

    def format_time(seconds):
        mins, secs = divmod(seconds, 60)
        return f"{mins:02d}:{secs:02d}"

    def update_timer():
        timer_text.value = format_time(remaining_time)
        total = break_duration if is_break else work_duration
        progress_ring.value = 1 - (remaining_time / total)
        progress_ring.color = ft.Colors.LIGHT_GREEN_ACCENT if is_break else ft.Colors.LIGHT_BLUE_ACCENT
        page.update()

    # --- FUNCIONALIDAD PRINCIPAL ---
    async def run_timer():
        nonlocal remaining_time, is_running, is_break
        while is_running and remaining_time > 0:
            await asyncio.sleep(1)
            remaining_time -= 1
            update_timer()

        # Cuando se acaba el tiempo
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

    # --- ACCIONES DE BOTONES ---
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
            page.snack_bar.open = True
            page.update()
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("⚠️ Introduce números válidos"))
            page.snack_bar.open = True
            page.update()

    btn_aplicar = ft.ElevatedButton(
        text="Aplicar",
        bgcolor="#1E90FF",
        color=ft.Colors.WHITE,
        on_click=aplicar_config,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
    )

    configuracion = ft.Row(
        [tiempo_concentracion, tiempo_descanso, btn_aplicar],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15
    )

    # --- BOTONES DE CONTROL ---
    btn_iniciar = ft.ElevatedButton(
        text="Iniciar",
        bgcolor="#1E90FF",
        color=ft.Colors.WHITE,
        width=120,
        height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        on_click=start_timer
    )

    btn_pausar = ft.ElevatedButton(
        text="Pausar",
        bgcolor="#FF8C00",
        color=ft.Colors.WHITE,
        width=120,
        height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        on_click=pause_timer
    )

    btn_reiniciar = ft.ElevatedButton(
        text="Reiniciar",
        bgcolor="#B22222",
        color=ft.Colors.WHITE,
        width=120,
        height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        on_click=reset_timer
    )

    botones_row = ft.Row(
        [btn_iniciar, btn_pausar, btn_reiniciar],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=25
    )

    # --- ESTRUCTURA VISUAL ---
    header = ft.Row([ft.Container(expand=True), btn_home], alignment=ft.MainAxisAlignment.END)

    content = ft.Column(
        [
            header,
            ft.Container(height=40),
            ft.Text("Pomodoro", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Container(height=20),
            configuracion,
            ft.Container(height=40),
            estado_texto,
            ft.Stack(
                [
                    progress_ring,
                    ft.Container(timer_text, alignment=ft.alignment.center),
                ],
                alignment=ft.alignment.center,
                width=300,
                height=200,
            ),
            ft.Container(height=30),
            botones_row
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    layout = ft.Container(
        expand=True,
        padding=ft.padding.all(30),
        content=content
    )

    update_timer()
    return layout
