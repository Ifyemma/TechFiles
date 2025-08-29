import flet as ft
import random

def main(page: ft.Page):
    page.title = "Weather Simulator"
    weather_text = ft.Text("Click to simulate weather", size=20)

    def simulate(e):
        weather = random.choice(["☀️ Sunny", "🌧️ Rainy", "☁️ Cloudy", "⛈️ Stormy"])
        weather_text.value = f"Weather: {weather}"
        page.update()

    page.add(weather_text, ft.ElevatedButton("Simulate", on_click=simulate))

ft.app(target=main)
