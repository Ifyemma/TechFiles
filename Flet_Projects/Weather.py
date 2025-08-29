import flet as ft
import requests

API_KEY = "your_api_key_here"  # Get from openweathermap.org

def main(page: ft.Page):
    page.title = "Weather App"
    city_input = ft.TextField(label="Enter city", width=300)
    result = ft.Text()

    def get_weather(e):
        city = city_input.value
        if city:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            res = requests.get(url).json()
            if res.get("main"):
                temp = res["main"]["temp"]
                desc = res["weather"][0]["description"]
                result.value = f"Temperature: {temp}°C, {desc.title()}"
            else:
                result.value = "City not found."
            page.update()

    page.add(city_input, ft.ElevatedButton("Get Weather", on_click=get_weather), result)

ft.app(target=main)
