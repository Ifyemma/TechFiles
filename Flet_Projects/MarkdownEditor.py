import flet as ft
import markdown

def main(page: ft.Page):
    editor = ft.TextField(multiline=True, min_lines=10, expand=True)
    preview = ft.Text("", selectable=True)

    def update_preview(e):
        html = markdown.markdown(editor.value)
        preview.value = html
        page.update()

    editor.on_change = update_preview
    page.add(
        ft.Text("Markdown Editor", style="headlineSmall"),
        editor,
        ft.Text("Preview:", style="titleSmall"),
        preview
    )

ft.app(target=main)
