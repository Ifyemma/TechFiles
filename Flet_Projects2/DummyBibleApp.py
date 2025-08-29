import flet as ft

# Dummy books for now (we'll load real ones later)
BOOKS = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"]

def main(page: ft.Page):
    page.title = "Bible App"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = "auto"
    
    selected_book = ft.Dropdown(
        label="Select Book",
        options=[ft.dropdown.Option(book) for book in BOOKS],
        width=300,
    )

    selected_chapter = ft.Dropdown(
        label="Select Chapter",
        options=[ft.dropdown.Option(str(i)) for i in range(1, 51)],
        width=300,
    )

    verse_display = ft.Text("Select a book and chapter to view verses.", selectable=True)

    def on_selection_change(e):
        if selected_book.value and selected_chapter.value:
            verse_display.value = f"📖 Displaying {selected_book.value} Chapter {selected_chapter.value}...\n(Real verses will show here soon)"
            page.update()

    selected_book.on_change = on_selection_change
    selected_chapter.on_change = on_selection_change

    page.add(
        ft.Column([
            ft.Row([selected_book, selected_chapter]),
            ft.Divider(),
            verse_display,
        ])
    )

ft.app(target=main)
