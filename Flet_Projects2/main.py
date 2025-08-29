import flet as ft
import os
from db import init_db, add_book, get_books, get_book_file, save_progress, get_progress
from PyPDF2 import PdfReader
from ebooklib import epub
from bs4 import BeautifulSoup

PAGE_SIZE = 800
BOOKS_DIR = "books"

if not os.path.exists(BOOKS_DIR):
    os.makedirs(BOOKS_DIR)

def main(page: ft.Page):
    page.title = "📚 Book App"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = "auto"
    init_db()

    current_book_id = None
    current_page = 0
    pages = []
    search_matches = []
    match_index = 0

    # UI
    book_list = ft.Column()
    content_display = ft.Text("", selectable=True, size=16)
    page_info = ft.Text("")
    search_box = ft.TextField(label="🔍 Search library", expand=True)

    # --- Library Functions ---
    def load_books(_=None):
        book_list.controls.clear()
        books = get_books()
        for b in books:
            btn = ft.ElevatedButton(
                f"{b[1]} - {b[2]}",
                on_click=lambda e, bid=b[0]: open_book(bid)
            )
            book_list.controls.append(btn)
        page.update()

    def parse_file(file_path):
        """Read TXT, PDF, EPUB files and return content as string."""
        ext = os.path.splitext(file_path)[1].lower()
        text = ""

        if ext == ".txt":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        elif ext == ".pdf":
            reader = PdfReader(file_path)
            for p in reader.pages:
                txt = p.extract_text()
                if txt:
                    text += txt + "\n"
        elif ext == ".epub":
            book = epub.read_epub(file_path)
            for item in book.items:
                if item.get_type() == epub.EpubHtml:
                    soup = BeautifulSoup(item.get_body_content(), "html.parser")
                    text += soup.get_text() + "\n"

        return text if text.strip() else "❌ Unable to read file."

    def open_book(book_id):
        nonlocal current_book_id, current_page, pages, search_matches, match_index
        current_book_id = book_id
        file_path = get_book_file(book_id)
        content = parse_file(file_path)
        pages = [content[i:i+PAGE_SIZE] for i in range(0, len(content), PAGE_SIZE)]
        search_matches = []
        match_index = 0
        current_page = get_progress(book_id)
        show_page()
        tabs.selected_index = 1
        page.update()

    # --- Reader Functions ---
    def show_page():
        if pages:
            content_display.value = pages[current_page]
            page_info.value = f"Page {current_page+1} of {len(pages)}"
            save_progress(current_book_id, current_page)
        page.update()

    def next_page(e):
        nonlocal current_page
        if current_page < len(pages)-1:
            current_page += 1
            show_page()

    def prev_page(e):
        nonlocal current_page
        if current_page > 0:
            current_page -= 1
            show_page()

    # --- Search Inside Book ---
    search_field = ft.TextField(label="🔍 Search in book", expand=True)
    match_info = ft.Text("")

    def search_in_book(e):
        nonlocal search_matches, match_index, current_page
        keyword = search_field.value.strip().lower()
        search_matches = []
        match_index = 0
        if not keyword or not pages:
            match_info.value = "No search keyword."
            page.update()
            return

        for i, p in enumerate(pages):
            if keyword in p.lower():
                search_matches.append(i)

        if search_matches:
            match_index = 0
            current_page = search_matches[match_index]
            match_info.value = f"Found {len(search_matches)} matches. Showing {match_index+1}."
            show_page()
        else:
            match_info.value = "No matches found."
        page.update()

    def next_match(e):
        nonlocal match_index, current_page
        if search_matches:
            match_index = (match_index + 1) % len(search_matches)
            current_page = search_matches[match_index]
            match_info.value = f"Match {match_index+1} of {len(search_matches)}"
            show_page()

    def prev_match(e):
        nonlocal match_index, current_page
        if search_matches:
            match_index = (match_index - 1) % len(search_matches)
            current_page = search_matches[match_index]
            match_info.value = f"Match {match_index+1} of {len(search_matches)}"
            show_page()

    # --- File Upload ---
    def file_upload_result(e: ft.FilePickerResultEvent):
        if e.files:
            file = e.files[0]
            file_path = os.path.join(BOOKS_DIR, file.name)
            page.get_upload_url(file, file_path)  # placeholder
            add_book(file.name, "Unknown Author", file_path)
            load_books()

    file_picker = ft.FilePicker(on_result=file_upload_result)
    page.overlay.append(file_picker)

    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        page.update()

    # --- Tabs ---
    library_tab = ft.Column([
        ft.Row([search_box, ft.IconButton(ft.icons.REFRESH, on_click=load_books)]),
        ft.Text("Library", size=20, weight="bold"),
        book_list,
        ft.ElevatedButton("➕ Upload Book", on_click=lambda _: file_picker.pick_files(
            allow_multiple=False, allowed_extensions=["txt", "pdf", "epub"]))
    ], expand=True)

    reader_tab = ft.Column([
        search_field,
        ft.Row([
            ft.ElevatedButton("Search", on_click=search_in_book),
            ft.ElevatedButton("⬅️ Prev Match", on_click=prev_match),
            ft.ElevatedButton("Next Match ➡️", on_click=next_match),
        ]),
        match_info,
        content_display,
        ft.Row([
            ft.ElevatedButton("⬅️ Prev Page", on_click=prev_page),
            page_info,
            ft.ElevatedButton("Next Page ➡️", on_click=next_page),
        ])
    ], expand=True)

    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="📚 Library", content=library_tab),
            ft.Tab(text="📖 Reader", content=reader_tab),
        ],
        expand=True
    )

    page.add(
        ft.Row([
            ft.IconButton(ft.icons.BRIGHTNESS_6, on_click=toggle_theme),
            ft.Text("Book App", size=24, weight="bold"),
        ]),
        tabs
    )

    load_books()

ft.app(target=main)
