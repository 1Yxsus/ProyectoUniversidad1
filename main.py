import flet as ft
from app.views.login_view import LoginView
from app.views.register_view import RegisterView
from app.views.home_view import HomeView
from app.views.dashboard_view import DashboardView
from app.views.options_view import DashboardOptionsView
from app.views.aula_dashboard import AulaDashboardView
from app.views.herramientas_view import ToolsDashboardView
from app.views.pomodoro_view import PomodoroView
from app.views.tus_aulas_view import AulasView
from app.views.probar_syllabus import TestGeminiView


def main(page: ft.Page):
    
    def route_change(route):
        page.views.clear()

        if page.route == "/":
            page.views.append(ft.View("/", [HomeView(page)]))
        elif page.route == "/login":
            page.views.append(ft.View("/login", [LoginView(page)]))
        elif page.route == "/register":
            page.views.append(ft.View("/register", [RegisterView(page)]))
        elif page.route == "/dashboard":
            page.views.append(ft.View("/dashboard", [DashboardView(page, username="Estudiante UNFV")]))
        elif page.route == "/options":
            page.views.append(ft.View("/options", [DashboardOptionsView(page)]))
        elif page.route == "/aula_dashboard":
            page.views.append(ft.View("/aula_dashboard", [AulaDashboardView(page)]))
        elif page.route == "/herramientas":
            page.views.append(ft.View("/herramientas", [ToolsDashboardView(page)]))
        elif page.route == "/pomodoro":
            page.views.append(ft.View("/pomodoro", [PomodoroView(page)]))
        elif page.route == "/tus_aulas":
            page.views.append(ft.View("/tus_aulas", [AulasView(page)]))
        elif page.route == "/test_syllabus":
            page.views.append(ft.View("/test_syllabus", [TestGeminiView(page)]))

        
        page.update()


    page.on_route_change = route_change
    page.go(page.route)


ft.app(target=main) #assets_dir="assets", view=ft.WEB_BROWSER)
