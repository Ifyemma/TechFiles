import flet as ft
from datetime import datetime

habits = {"Drink Water": False, "Exercise": False, "Read": False}

def main(page: ft.Page):
    page.title = f"Habits for {datetime.today().strftime('%Y-%m-%d')}"
    habit_column = ft.Column()

    def toggle_habit(habit):
        def handler(e):
            habits[habit] = not habits[habit]
            update_ui()
        return handler

    def update_ui():
        habit_column.controls.clear()
        for h, done in habits.items():
            habit_column.controls.append(
                ft.Checkbox(label=h, value=done, on_change=toggle_habit(h))
            )
        page.update()

    update_ui()
    page.add(ft.Text("Daily Habit Tracker", style="headlineMedium"), habit_column)

ft.app(target=main)
