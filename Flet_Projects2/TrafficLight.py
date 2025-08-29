import flet as ft
import time

def main(page: ft.Page):
    page.title = "Traffic Light Simulator"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    red = ft.Container(width=100, height=100, bgcolor="grey", border_radius=50)
    yellow = ft.Container(width=100, height=100, bgcolor="grey", border_radius=50)
    green = ft.Container(width=100, height=100, bgcolor="grey", border_radius=50)

    def run_cycle(e):
        while True:
            red.bgcolor, yellow.bgcolor, green.bgcolor = "red", "grey", "grey"
            page.update()
            time.sleep(3)

            red.bgcolor, yellow.bgcolor, green.bgcolor = "grey", "yellow", "grey"
            page.update()
            time.sleep(2)

            red.bgcolor, yellow.bgcolor, green.bgcolor = "grey", "grey", "green"
            page.update()
            time.sleep(3)

    page.add(ft.Row([red, yellow, green], alignment="center"))
    page.add(ft.ElevatedButton("Start", on_click=run_cycle))

ft.app(target=main)
