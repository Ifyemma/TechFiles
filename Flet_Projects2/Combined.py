import flet as ft
import random
import time
import threading

def main(page: ft.Page):
    page.title = "Simulator Hub"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    # ===================== 1. TRAFFIC LIGHT =====================
    def traffic_light_view():
        red = ft.Container(width=100, height=100, bgcolor="grey", border_radius=50)
        yellow = ft.Container(width=100, height=100, bgcolor="grey", border_radius=50)
        green = ft.Container(width=100, height=100, bgcolor="grey", border_radius=50)

        def run_cycle(e):
            def loop():
                while True:
                    red.bgcolor, yellow.bgcolor, green.bgcolor = "red", "grey", "grey"
                    page.update()
                    time.sleep(2)
                    red.bgcolor, yellow.bgcolor, green.bgcolor = "grey", "yellow", "grey"
                    page.update()
                    time.sleep(2)
                    red.bgcolor, yellow.bgcolor, green.bgcolor = "grey", "grey", "green"
                    page.update()
                    time.sleep(2)
            threading.Thread(target=loop, daemon=True).start()

        return ft.Column([
            ft.Row([red, yellow, green], alignment="center"),
            ft.ElevatedButton("Start Traffic Light", on_click=run_cycle)
        ], alignment="center", horizontal_alignment="center")

    # ===================== 2. ATM =====================
    def atm_view():
        user_balance = {"amount": 1000}
        balance = ft.Text(f"Balance: ${user_balance['amount']}", size=20)
        amount = ft.TextField(label="Enter Amount", width=200)

        def deposit(e):
            user_balance["amount"] += int(amount.value or 0)
            balance.value = f"Balance: ${user_balance['amount']}"
            page.update()

        def withdraw(e):
            if int(amount.value or 0) <= user_balance["amount"]:
                user_balance["amount"] -= int(amount.value or 0)
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Insufficient Funds!"))
                page.snack_bar.open = True
            balance.value = f"Balance: ${user_balance['amount']}"
            page.update()

        return ft.Column([
            balance,
            amount,
            ft.Row([
                ft.ElevatedButton("Deposit", on_click=deposit),
                ft.ElevatedButton("Withdraw", on_click=withdraw)
            ])
        ], alignment="center")

    # ===================== 3. WEATHER =====================
    def weather_view():
        weather_text = ft.Text("Click to simulate weather", size=20)

        def simulate(e):
            weather = random.choice(["☀️ Sunny", "🌧️ Rainy", "☁️ Cloudy", "⛈️ Stormy"])
            weather_text.value = f"Weather: {weather}"
            page.update()

        return ft.Column([
            weather_text,
            ft.ElevatedButton("Simulate Weather", on_click=simulate)
        ], alignment="center")

    # ===================== 4. ELEVATOR =====================
    def elevator_view():
        floor_display = ft.Text("Floor: 0", size=25)
        current_floor = {"floor": 0}

        def move_to(floor):
            while current_floor["floor"] != floor:
                if current_floor["floor"] < floor:
                    current_floor["floor"] += 1
                else:
                    current_floor["floor"] -= 1
                floor_display.value = f"Floor: {current_floor['floor']}"
                page.update()
                time.sleep(1)

        def call_floor(e):
            threading.Thread(target=move_to, args=(int(e.control.text),), daemon=True).start()

        buttons = ft.Row([
            ft.ElevatedButton(str(i), on_click=call_floor) for i in range(6)
        ])

        return ft.Column([floor_display, buttons], alignment="center")

    # ===================== 5. STOCK MARKET =====================
    def stock_view():
        price = {"value": 100}
        price_text = ft.Text(f"Stock Price: ${price['value']}", size=25)

        def update_price():
            while True:
                price["value"] += random.randint(-5, 5)
                if price["value"] < 1:
                    price["value"] = 1
                price_text.value = f"Stock Price: ${price['value']}"
                page.update()
                time.sleep(2)

        threading.Thread(target=update_price, daemon=True).start()
        return ft.Column([price_text], alignment="center")

    # ===================== NAVIGATION =====================
    content = ft.Column([], alignment="center", expand=True)

    def show_view(view):
        content.controls.clear()
        if view == "Traffic Light":
            content.controls.append(traffic_light_view())
        elif view == "ATM":
            content.controls.append(atm_view())
        elif view == "Weather":
            content.controls.append(weather_view())
        elif view == "Elevator":
            content.controls.append(elevator_view())
        elif view == "Stock":
            content.controls.append(stock_view())
        page.update()

    sidebar = ft.Column([
        ft.Text("Simulator Hub", size=25, weight="bold"),
        ft.ElevatedButton("Traffic Light", on_click=lambda e: show_view("Traffic Light")),
        ft.ElevatedButton("ATM", on_click=lambda e: show_view("ATM")),
        ft.ElevatedButton("Weather", on_click=lambda e: show_view("Weather")),
        ft.ElevatedButton("Elevator", on_click=lambda e: show_view("Elevator")),
        ft.ElevatedButton("Stock Market", on_click=lambda e: show_view("Stock")),
    ], spacing=10)

    page.add(ft.Row([sidebar, ft.VerticalDivider(), content], expand=True))

ft.app(target=main)
