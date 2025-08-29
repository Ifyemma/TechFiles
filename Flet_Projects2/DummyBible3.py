import flet as ft
import sqlite3

# Connect to the SQLite Bible DB
conn = sqlite3.connect("kjv_bible.db")
cursor = conn.cursor()

# Functions
def get_books():
    cursor.execute("SELECT DISTINCT book FROM bible")
    return [row[0] for row in cursor.fetchall()]

def get_chapters(book):
    cursor.execute("SELECT DISTINCT chapter FROM bible WHERE book = ?", (book,))
    return [str(row[0]) for row in cursor.fetchall()]

def get_verses(book, chapter):
    cursor.execute("SELECT verse, text FROM bible WHERE book = ? AND chapter = ?", (book, chapter))
    return cursor.fetchall()

def search_verses(keyword):
    cursor.execute("SELECT book, chapter, verse, text FROM bible WHERE text LIKE ?", ('%' + keyword + '%',))
    return cursor.fetchall()

def main(page: ft.Page):
    page.title = "Bible App (KJV)"
    page.scroll = "auto"
    page.theme_mode = ft.ThemeMode.LIGHT

    # UI Elements
    book_dropdown = ft.Dropdown(label="Book", width=300)
    chapter_dropdown = ft.Dropdown(label="Chapter", width=300)
    verse_display = ft.Text(value="Select a book and chapter to load verses.", selectable=True, max_lines=999)

    # Load books
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
            search_results.value = ""
            page.update()

    book_dropdown.on_change = on_book_change
    chapter_dropdown.on_change = on_chapter_change

    # Search Area
    search_input = ft.TextField(label="Search Bible (e.g. faith, Jesus)", width=300)
    search_results = ft.Text(value="", selectable=True, max_lines=999)

    def on_search(e):
        keyword = search_input.value.strip()
        if keyword:
            results = search_verses(keyword)
            if results:
                display = f"🔍 Search Results for '{keyword}' ({len(results)} found):\n\n"
                for book, chapter, verse, text in results[:200]:  # limit to 200
                    display += f"{book} {chapter}:{verse} - {text}\n"
            else:
                display = f"No results found for '{keyword}'."
            search_results.value = display
            verse_display.value = ""
            page.update()

    search_btn = ft.ElevatedButton(text="Search", on_click=on_search)

    # Layout
    page.add(
        ft.Column([
            ft.Row([book_dropdown, chapter_dropdown]),
            ft.Divider(),
            verse_display,
            ft.Divider(),
            ft.Row([search_input, search_btn]),
            search_results
        ])
    )

ft.app(target=main)
