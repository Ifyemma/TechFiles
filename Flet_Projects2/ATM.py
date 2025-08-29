import flet as ft

def main(page: ft.Page):
    page.title = "ATM Simulator"
    balance = ft.Text("Balance: $1000", size=20)
    user_balance = 1000
    amount = ft.TextField(label="Enter Amount", width=200)

    def deposit(e):
        nonlocal user_balance
        user_balance += int(amount.value)
        balance.value = f"Balance: ${user_balance}"
        page.update()

    def withdraw(e):
        nonlocal user_balance
        if int(amount.value) <= user_balance:
            user_balance -= int(amount.value)
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Insufficient Funds!"))
            page.snack_bar.open = True
        balance.value = f"Balance: ${user_balance}"
        page.update()

    page.add(balance, amount,
             ft.Row([
                 ft.ElevatedButton("Deposit", on_click=deposit),
                 ft.ElevatedButton("Withdraw", on_click=withdraw)
             ]))

ft.app(target=main)
