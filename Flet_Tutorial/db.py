import sqlite3
import os
from datetime import datetime

DB_NAME = "blog.db"

def connect():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = connect()
    c = conn.cursor()
    
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Posts table
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT,
            image TEXT,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create default user
    c.execute("SELECT * FROM users WHERE username = 'admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', 'admin123'))

    conn.commit()
    conn.close()

def verify_user(username, password):
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = c.fetchone()
    conn.close()
    return result is not None

def save_post(title, content, category, image):
    conn = connect()
    c = conn.cursor()
    c.execute(
        "INSERT INTO posts (title, content, category, image) VALUES (?, ?, ?, ?)",
        (title, content, category, image)
    )
    conn.commit()
    conn.close()

def get_all_posts():
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT id, title, category, created FROM posts ORDER BY created DESC")
    results = c.fetchall()
    conn.close()
    return results

def get_post_by_id(post_id):
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT title, content, category, image FROM posts WHERE id = ?", (post_id,))
    result = c.fetchone()
    conn.close()
    return result

def get_full_post(post_id):
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT title, content, category, image, created FROM posts WHERE id = ?", (post_id,))
    result = c.fetchone()
    conn.close()
    return result

def update_post(post_id, title, content, category, image=None):
    conn = connect()
    c = conn.cursor()
    if image:
        c.execute(
            "UPDATE posts SET title = ?, content = ?, category = ?, image = ? WHERE id = ?",
            (title, content, category, image, post_id)
        )
    else:
        c.execute(
            "UPDATE posts SET title = ?, content = ?, category = ? WHERE id = ?",
            (title, content, category, post_id)
        )
    conn.commit()
    conn.close()

def delete_post(post_id):
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()

def get_published_posts():
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT id, title, content, category, image, created FROM posts ORDER BY created DESC")
    results = c.fetchall()
    conn.close()
    return results

def get_all_categories():
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT DISTINCT category FROM posts WHERE category IS NOT NULL AND category != ''")
    results = [row[0] for row in c.fetchall()]
    conn.close()
    return results

def get_posts_by_category(category):
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT id, title, content, category, image, created FROM posts WHERE category = ? ORDER BY created DESC", (category,))
    results = c.fetchall()
    conn.close()
    return results

def search_posts(keyword):
    conn = connect()
    c = conn.cursor()
    query = f"""
        SELECT id, title, content, category, image, created
        FROM posts
        WHERE title LIKE ? OR content LIKE ? OR category LIKE ?
        ORDER BY created DESC
    """
    like_pattern = f"%{keyword}%"
    c.execute(query, (like_pattern, like_pattern, like_pattern))
    results = c.fetchall()
    conn.close()
    return results
