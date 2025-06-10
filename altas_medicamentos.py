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
        print(f"Error al inicializar Firebase: {e}")

db = firestore.client()

def main(page: ft.Page):

    def regresar_al_menu(e):
        page.clean()
        import app  # Cambia a 'main' si tu archivo principal se llama main.py
        app.main(page)

    def guardar_medicamento(e: ft.ControlEvent):
        clave = txt_clave.value.strip()
        nombre = txt_descripcion.value.strip()
        presentacion = txt_presentacion.value.strip()
        clasificacion = drp_clasificacion.value
        nivel = drp_nivel.value
        farmaco = drp_farmaco.value

        if clave == "":
            page.open(ft.SnackBar(ft.Text("Introduce la clave")))
            return
        if nombre == "":
            page.open(ft.SnackBar(ft.Text("Introduce el nombre")))
            return
        if presentacion == "":
            page.open(ft.SnackBar(ft.Text("Introduce la presentación")))
            return
        if clasificacion is None:
            page.open(ft.SnackBar(ft.Text("Selecciona la clasificación")))
            return
        if nivel is None:
            page.open(ft.SnackBar(ft.Text("Selecciona el nivel de atención")))
            return

        db.collection("medicamento").add({
            "clave": clave,
            "descripcion": nombre,
            "presentacion": presentacion,
            "clasificacion": clasificacion,
            "nivel_atencion": nivel,
            "nombre_farmaco": farmaco
        })

        page.open(ft.SnackBar(ft.Text("Guardado correctamente"), bgcolor="blue", show_close_icon=True))

    # Configuración general
    page.title = "Alta de medicamentos"
    page.theme_mode = "light"
    page.window_width = 200
    page.window_height = 350
    page.window_resizable = False

    page.appbar = ft.AppBar(
        leading=ft.Icon("medical_services"),
        title=ft.Text("Nuevo medicamento"),
        center_title=True,
        bgcolor="green",
        color="white",
        actions=[
            ft.Image(src="logo.png", width=80, height=80, color="white"),
            ft.IconButton(icon=ft.icons.EXIT_TO_APP, tooltip="Regresar", on_click=regresar_al_menu)
        ]
    )

    txt_clave = ft.TextField(label="Clave", width=200, border="underline", filled=True, value="S/C")
    txt_descripcion = ft.TextField(label="Nombre y Descripción del medicamento", multiline=True, min_lines=1, max_lines=3, width=350)
    txt_presentacion = ft.TextField(label="Presentación", multiline=True, min_lines=1, max_lines=3, width=350)

    # Clasificaciones desde Firestore
    clasificaciones_set = set()
    medicamentos = db.collection("medicamento").stream()
    for doc in medicamentos:
        data = doc.to_dict()
        clas = data.get("clasificacion")
        if clas:
            clasificaciones_set.add(clas)

    lista_clasificacion = [ft.dropdown.Option(c) for c in sorted(clasificaciones_set)]
    drp_clasificacion = ft.Dropdown(options=lista_clasificacion, width=350, label="Clasificación")

    # Nivel de atención
    lista_nivel = [
        ft.dropdown.Option("Nivel 1"),
        ft.dropdown.Option("Nivel 2"),
        ft.dropdown.Option("Nivel 3"),
        ft.dropdown.Option("Nivel 1 y 2"),
        ft.dropdown.Option("Nivel 1 y 3"),
        ft.dropdown.Option("Nivel 2 y 3"),
        ft.dropdown.Option("Nivel 1, 2 y 3")
    ]
    drp_nivel = ft.Dropdown(options=lista_nivel, width=350, label="Nivel de atención")

    # Fármacos desde Firestore
    lista_farmaco = []
    farmacos = db.collection("farmaco").stream()
    for doc in farmacos:
        nombre = doc.to_dict().get("nombre", "")
        if nombre:
            lista_farmaco.append(ft.dropdown.Option(nombre))
    drp_farmaco = ft.Dropdown(options=lista_farmaco, width=350, label="Fármaco o sustancia activa")

    btn_guardar = ft.ElevatedButton(
        text="Guardar",
        icon="save",
        icon_color="white",
        bgcolor="blue",
        color="white",
        width=150,
        on_click=guardar_medicamento
    )

    btn_cancelar = ft.ElevatedButton(
        text="Cancelar",
        icon="close",
        icon_color="white",
        bgcolor="red",
        color="white",
        width=150
    )

    fila_boton = ft.Row([btn_guardar, btn_cancelar])

    page.add(
        txt_clave,
        txt_descripcion,
        txt_presentacion,
        drp_clasificacion,
        drp_nivel,
        drp_farmaco,
        fila_boton
    )
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
