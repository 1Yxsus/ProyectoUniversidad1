import flet as ft
from app.controllers.aulas_usuario_controller import obtener_rol_usuario_en_aula

    # ------------------------------------------------------
    # --- USUARIO Y ROL (para controlar permisos) ---
    # ------------------------------------------------------
def is_staff_verification(page: ft.Page, id_aula: int) -> bool:
    roles_by_aula = page.session.get("roles_by_aula") or {}
    # obtener id del aula de forma segura
    id_aula_raw = id_aula
    try:
        id_aula_int = int(id_aula_raw) if id_aula_raw is not None else None
    except Exception:
        id_aula_int = None

    # intentar obtener role desde session (acepta claves int o str)
    role = None
    if roles_by_aula:
        if id_aula_int is not None and id_aula_int in roles_by_aula:
            role = roles_by_aula.get(id_aula_int)
        else:
            role = roles_by_aula.get(str(id_aula_int)) or roles_by_aula.get(str(id_aula_raw))

    # si no encontramos role en session, pedirlo al controlador (seguro)
    if not role and id_aula_int is not None:
        current_user = page.session.get("user") or {}
        uid = current_user.get("id_usuario")
        if uid:
            try:
                role = obtener_rol_usuario_en_aula(id_aula_int, uid)
            except Exception:
                role = None

    is_staff = (role or "").upper() in ("ADMIN", "PROFESOR", "DOCENTE")

    return is_staff