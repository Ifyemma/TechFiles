import flet as ft

tasks = []

def main(page: ft.Page):
    page.title = "To-Do List"
    task_column = ft.Column()

    task_input = ft.TextField(label="New Task", width=300)

    def add_task(e):
        if task_input.value:
            tasks.append({"text": task_input.value, "done": False})
            task_input.value = ""
            update_tasks()

    def toggle_done(index):
        def handler(e):
            tasks[index]["done"] = not tasks[index]["done"]
            update_tasks()
        return handler

    def update_tasks():
        task_column.controls.clear()
        for i, task in enumerate(tasks):
            task_column.controls.append(
                ft.Checkbox(
                    label=task["text"],
                    value=task["done"],
                    on_change=toggle_done(i)
                )
            )
        page.update()

    page.add(task_input, ft.ElevatedButton("Add", on_click=add_task), ft.Divider(), task_column)

ft.app(target=main)

--------------------------------------------------------------------------------

2. Chat Application (Local Only)
pythonCopy codeimport flet as ft

messages = []

def main(page: ft.Page):
    page.title = "Local Chat"
    chat_display = ft.Column(scroll=ft.ScrollMode.ALWAYS)
    name_input = ft.TextField(label="Your name", width=200)
    msg_input = ft.TextField(label="Type a message...", expand=True)

    def send_msg(e):
        if name_input.value and msg_input.value:
            messages.append(f"{name_input.value}: {msg_input.value}")
            msg_input.value = ""
            update_chat()

    def update_chat():
        chat_display.controls.clear()
        for msg in messages:
            chat_display.controls.append(ft.Text(msg))
        page.update()

    page.add(
        ft.Row([name_input]),
        ft.Row([msg_input, ft.ElevatedButton("Send", on_click=send_msg)]),
        ft.Divider(),
        chat_display
    )

ft.app(target=main)
