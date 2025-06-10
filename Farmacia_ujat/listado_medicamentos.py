import flet as ft
import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar conexión con Firestore (haz esto una sola vez)
if not firebase_admin._apps:
    cred = credentials.Certificate("farmacia-ujat-firebase-adminsdk-fbsvc-5a1534d9ec.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

def main(page: ft.Page):
    page.title = "Listado de medicamentos UJAT"
    page.window_width = 900
    page.window_height = 600
    page.scroll = True
    page.theme_mode = "light"
    page.appbar = ft.AppBar(
        title=ft.Text("Listado de medicamentos UJAT"),
        leading=ft.Icon("receipt_long"),
        bgcolor="blue",
        center_title=True,
    )

    encabezado = [
        ft.DataColumn(ft.Text("Descripción", width=200)),
        ft.DataColumn(ft.Text("Presentación", width=200)),
        ft.DataColumn(ft.Text("Clasificación", width=200)),
        ft.DataColumn(ft.Text("Nivel de atención", width=100)),
        ft.DataColumn(ft.Text("Sustancia activa", width=200))
    ]

    filas = []

    # 🔁 Leer medicamentos desde Firestore
    medicamentos = db.collection("medicamento").stream()
    for doc in medicamentos:
        data = doc.to_dict()
        celda1 = ft.DataCell(ft.Text(data.get("descripcion", ""), weight="bold"))
        celda2 = ft.DataCell(ft.Text(data.get("presentacion", "")))
        celda3 = ft.DataCell(ft.Text(data.get("clasificacion", ""), italic=True))
        celda4 = ft.DataCell(ft.Text(data.get("nivel_atencion", "")))
        celda5 = ft.DataCell(ft.Text(data.get("nombre_farmaco", ""), color="pink"))  # nombre del farmaco

        fila = ft.DataRow([celda1, celda2, celda3, celda4, celda5])
        filas.append(fila)

    tabla = ft.DataTable(columns=encabezado, rows=filas)
    page.add(tabla)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
