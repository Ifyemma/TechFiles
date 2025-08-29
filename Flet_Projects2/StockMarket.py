import flet as ft
import random
import time
import threading

def main(page: ft.Page):
    page.title = "Stock Market Simulator"
    price = 100
    price_text = ft.Text(f"Stock Price: ${price}", size=25)

    def update_price():
        nonlocal price
        while True:
            price += random.randint(-5, 5)
            if price < 1:
                price = 1
            price_text.value = f"Stock Price: ${price}"
            page.update()
            time.sleep(2)

    threading.Thread(target=update_price, daemon=True).start()
    page.add(price_text)

ft.app(target=main)
