import flet as ft

transactions = []

def main(page: ft.Page):
    page.title = "Budget Tracker"
    page.scroll = True

    transaction_list = ft.Column()

    amount_input = ft.TextField(label="Amount", width=200)
    desc_input = ft.TextField(label="Description", width=300)
    type_dropdown = ft.Dropdown(
        label="Type",
        width=150,
        options=[
            ft.dropdown.Option("Income"),
            ft.dropdown.Option("Expense"),
        ]
    )

    total_income = 0
    total_expense = 0
    balance_text = ft.Text("", size=16, weight="bold")

    def update_summary():
        nonlocal total_income, total_expense
        total_income = sum(t["amount"] for t in transactions if t["type"] == "Income")
        total_expense = sum(t["amount"] for t in transactions if t["type"] == "Expense")
        balance = total_income - total_expense

        balance_text.value = f"Balance: ${balance:.2f} | Income: ${total_income:.2f} | Expenses: ${total_expense:.2f}"

    def add_transaction(e):
        try:
            amount = float(amount_input.value)
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Please enter a valid amount."))
            page.snack_bar.open = True
            page.update()
            return

        if not desc_input.value or not type_dropdown.value:
            page.snack_bar = ft.SnackBar(ft.Text("Please fill in all fields."))
            page.snack_bar.open = True
            page.update()
            return

        transactions.append({
            "amount": amount,
            "description": desc_input.value,
            "type": type_dropdown.value
        })

        # Clear inputs
        amount_input.value = ""
        desc_input.value = ""
        type_dropdown.value = None

        update_ui()

    def update_ui():
        transaction_list.controls.clear()
        for t in reversed(transactions):
            transaction_list.controls.append(
                ft.ListTile(
                    title=ft.Text(f"{t['description']}"),
                    subtitle=ft.Text(t['type']),
                    trailing=ft.Text(
                        f"${t['amount']:.2f}",
                        color="green" if t["type"] == "Income" else "red"
                    )
                )
            )
        update_summary()
        page.update()

    page.add(
        ft.Text("Personal Budget Tracker", style="headlineMedium"),
        ft.Row([amount_input, desc_input, type_dropdown]),
        ft.ElevatedButton("Add Transaction", on_click=add_transaction),
        ft.Divider(),
        balance_text,
        transaction_list
    )

    update_summary()

ft.app(target=main)
