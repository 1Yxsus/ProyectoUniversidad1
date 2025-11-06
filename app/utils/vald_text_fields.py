# utils/forms.py
import flet as ft

def validar_formulario(page: ft.Page, campos: list[ft.TextField], mensaje="Completa todos los campos."):
    valid = True
    for tf in campos:
        if not tf.value or not tf.value.strip():
            tf.error_text = "Requerido"
            valid = False
        else:
            tf.error_text = None
    page.update()

    if not valid:
        page.snack_bar = ft.SnackBar(ft.Text(f"⚠️ {mensaje}"), bgcolor="#FF5555")
        page.snack_bar.open = True
        page.update()

    return valid
