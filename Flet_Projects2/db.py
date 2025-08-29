import sqlite3

DB_NAME = "books.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            file_path TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            book_id INTEGER PRIMARY KEY,
            page INTEGER,
            FOREIGN KEY(book_id) REFERENCES books(id)
        )
    ''')
    conn.commit()
    conn.close()

def add_book(title, author, file_path):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, file_path) VALUES (?, ?, ?)",
                   (title, author, file_path))
    conn.commit()
    conn.close()

def get_books():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author, file_path FROM books")
    books = cursor.fetchall()
    conn.close()
    return books

def get_book_file(book_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT file_path FROM books WHERE id=?", (book_id,))
    file_path = cursor.fetchone()[0]
    conn.close()
    return file_path

def save_progress(book_id, page):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO progress (book_id, page) VALUES (?, ?)", (book_id, page))
    conn.commit()
    conn.close()

def get_progress(book_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT page FROM progress WHERE book_id=?", (book_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 0
