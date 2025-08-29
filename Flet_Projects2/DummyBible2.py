import flet as ft
import sqlite3

# Connect to Bible DB
conn = sqlite3.connect("Bible.db")  # Ensure this file is in the same folder
cursor = conn.cursor()

def get_books():
    cursor.execute("SELECT DISTINCT book FROM bible")
    return [row[0] for row in cursor.fetchall()]

def get_chapters(book):
    cursor.execute("SELECT DISTINCT chapter FROM bible WHERE book = ?", (book,))
    return [str(row[0]) for row in cursor.fetchall()]

def get_verses(book, chapter):
    cursor.execute("SELECT verse, text FROM bible WHERE book = ? AND chapter = ?", (book, chapter))
    return cursor.fetchall()

def main(page: ft.Page):
    page.title = "Bible App (KJV)"
    page.scroll = "auto"
    page.theme_mode = ft.ThemeMode.LIGHT

    book_dropdown = ft.Dropdown(label="Book", width=300)
    chapter_dropdown = ft.Dropdown(label="Chapter", width=300)
    verse_display = ft.Text(value="Select a book and chapter to load verses.", selectable=True, max_lines=999)

    # Load books into dropdown
    books = get_books()
    book_dropdown.options = [ft.dropdown.Option(book) for book in books]

    def on_book_change(e):
        book = book_dropdown.value
        chapters = get_chapters(book)
        chapter_dropdown.options = [ft.dropdown.Option(chap) for chap in chapters]
        chapter_dropdown.value = None
        page.update()

    def on_chapter_change(e):
        book = book_dropdown.value
        chapter = chapter_dropdown.value
        if book and chapter:
            verses = get_verses(book, int(chapter))
            display = f"📖 {book} Chapter {chapter}\n\n"
            for num, text in verses:
                display += f"{num}. {text}\n"
            verse_display.value = display
            page.update()

    book_dropdown.on_change = on_book_change
    chapter_dropdown.on_change = on_chapter_change

    page.add(
        ft.Column([
            ft.Row([book_dropdown, chapter_dropdown]),
            ft.Divider(),
            verse_display
        ])
    )

ft.app(target=main)
