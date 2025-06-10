import flet as ft
import os
import firebase_admin
from firebase_admin import credentials, firestore

# 🔐 Inicializar Firebase con ruta desde variable de entorno
cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
if cred_path and not firebase_admin._apps:
    try:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"Error al inicializar Firebase en interacciones: {e}")

db = firestore.client()

def main(page: ft.Page):

    def mostrar_interacciones(e: ft.ControlEvent):
        if e.control == drp_medicamentos1:
            desc = drp_medicamentos1.value
            txt = txt_interaccion1
        elif e.control == drp_medicamentos2:
            desc = drp_medicamentos2.value
            txt = txt_interaccion2
        elif e.control == drp_medicamentos3:
            desc = drp_medicamentos3.value
            txt = txt_interaccion3
        elif e.control == drp_medicamentos4:
            desc = drp_medicamentos4.value
            txt = txt_interaccion4
        elif e.control == drp_medicamentos5:
            desc = drp_medicamentos5.value
            txt = txt_interaccion5

        farmacos = db.collection("farmaco").stream()
        encontrado = False
        for doc in farmacos:
            data = doc.to_dict()
            nombre = data.get("nombre", "").lower()
            if nombre and nombre in desc.lower():
                txt.value = data.get("interacciones", "No registradas")
                encontrado = True
                break

        if not encontrado:
            txt.value = "No tiene en la BD"
        txt.update()

    def guardar_receta(e: ft.ControlEvent):
        if drp_medicamentos1.value is None:
            page.open(
                ft.SnackBar(
                    content=ft.Text("Selecciona el primer medicamento"),
                    bgcolor="red",
                    show_close_icon=True
                )
            )
            return

        for drp, txt in [
            (drp_medicamentos1, txt_interaccion1),
            (drp_medicamentos2, txt_interaccion2),
            (drp_medicamentos3, txt_interaccion3),
            (drp_medicamentos4, txt_interaccion4),
            (drp_medicamentos5, txt_interaccion5)
        ]:
            if drp.value:
                db.collection("receta").add({
                    "medicamento": drp.value,
                    "interaccion": txt.value
                })

        page.open(
            ft.SnackBar(
                content=ft.Text("Éxito"),
                bgcolor="blue",
                show_close_icon=True
            )
        )

        for drp in [drp_medicamentos1, drp_medicamentos2, drp_medicamentos3, drp_medicamentos4, drp_medicamentos5]:
            drp.value = None
            drp.update()
        for txt in [txt_interaccion1, txt_interaccion2, txt_interaccion3, txt_interaccion4, txt_interaccion5]:
            txt.value = ""
            txt.update()

    page.title = "Interacciones medicamentosas"
    page.theme_mode = "light"
    page.window_width = 800
    page.window_height = 600

   page.appbar = ft.AppBar(
    title=ft.Text("Interacciones UJAT", weight=ft.FontWeight.BOLD),
    leading=ft.Icon(ft.Icons.MEDICAL_SERVICES, color=ft.Colors.WHITE),
    actions=[
        ft.Image(src="logo.png", width=80, height=80, color="white"),
        ft.IconButton(icon=ft.icons.EXIT_TO_APP, tooltip="Regresar", on_click=regresar_al_menu)
    ],
    bgcolor=ft.Colors.DEEP_PURPLE_300,
    color="white",
    center_title=True
)


    lista = []
    medicamentos = db.collection("medicamento").stream()
    for doc in medicamentos:
        data = doc.to_dict()
        descripcion = data.get("descripcion", "")
        if descripcion:
            lista.append(ft.dropdown.Option(descripcion))

    txt_medicamentos = ft.Text("Medicamentos", size=20, color="white", italic=True, weight=ft.FontWeight.BOLD)
    div_medicamentos = ft.Divider(color=ft.Colors.WHITE, thickness=3)

    drp_medicamentos1 = ft.Dropdown(options=lista, label="Selecciona el medicamento 1", editable=True, enable_filter=True, on_change=mostrar_interacciones)
    drp_medicamentos2 = ft.Dropdown(options=lista, label="Selecciona el medicamento 2", editable=True, enable_filter=True, on_change=mostrar_interacciones)
    drp_medicamentos3 = ft.Dropdown(options=lista, label="Selecciona el medicamento 3", editable=True, enable_filter=True, on_change=mostrar_interacciones)
    drp_medicamentos4 = ft.Dropdown(options=lista, label="Selecciona el medicamento 4", editable=True, enable_filter=True, on_change=mostrar_interacciones)
    drp_medicamentos5 = ft.Dropdown(options=lista, label="Selecciona el medicamento 5", editable=True, enable_filter=True, on_change=mostrar_interacciones)

    col_medicamentos = ft.Column(
        [txt_medicamentos, div_medicamentos, drp_medicamentos1, drp_medicamentos2, drp_medicamentos3, drp_medicamentos4, drp_medicamentos5],
        expand=True, spacing=20
    )

    txt_interacciones = ft.Text("Interacciones", size=20, color="white", italic=True, weight=ft.FontWeight.BOLD)
    div_interacciones = ft.Divider(color=ft.Colors.WHITE, thickness=3)

    txt_interaccion1 = ft.TextField(label="Interacciones del medicamento 1", read_only=True)
    txt_interaccion2 = ft.TextField(label="Interacciones del medicamento 2", read_only=True)
    txt_interaccion3 = ft.TextField(label="Interacciones del medicamento 3", read_only=True)
    txt_interaccion4 = ft.TextField(label="Interacciones del medicamento 4", read_only=True)
    txt_interaccion5 = ft.TextField(label="Interacciones del medicamento 5", read_only=True)

    col_interacciones = ft.Column(
        [txt_interacciones, div_interacciones, txt_interaccion1, txt_interaccion2, txt_interaccion3, txt_interaccion4, txt_interaccion5],
        expand=True, spacing=20
    )

    row_componentes = ft.Row([col_medicamentos, col_interacciones], spacing=60)

    btn_aceptar = ft.ElevatedButton(
        text="Guardar",
        icon="cloud",
        icon_color="white",
        bgcolor=ft.Colors.TEAL_300,
        color="white",
        width=150,
        on_click=guardar_receta
    )

    btn_cancelar = ft.ElevatedButton(
        text="Cerrar",
        icon="close",
        icon_color="white",
        bgcolor=ft.Colors.INDIGO_400,
        color="white",
        width=150
    )

    row_botones = ft.Row([btn_aceptar, btn_cancelar], alignment="end", spacing=20)
    page.add(row_componentes, row_botones)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
