import flet as ft
import time

def main(page: ft.Page):
    page.title = "Elevator Simulator"
    floor_display = ft.Text("Floor: 0", size=25)
    current_floor = 0

    def move_to(floor):
        nonlocal current_floor
        while current_floor != floor:
            if current_floor < floor:
                current_floor += 1
            else:
                current_floor -= 1
            floor_display.value = f"Floor: {current_floor}"
            page.update()
            time.sleep(1)

    def call_floor(e):
        move_to(int(e.control.text))

    buttons = ft.Row([
        ft.ElevatedButton(str(i), on_click=call_floor) for i in range(6)
    ])

    page.add(floor_display, buttons)

ft.app(target=main)
