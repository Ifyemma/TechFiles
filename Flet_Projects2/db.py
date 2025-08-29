import sqlite3
import bcrypt

# --- Connect to SQLite DB ---
def init_db():
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()

    # Create users table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            category TEXT,
            image_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')


    # Create default admin if none exists
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if cursor.fetchone() is None:
        hashed = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", hashed))
        print("[✔] Default admin created: admin / admin123")

    conn.commit()
    conn.close()

def save_post(title, content, category, image_path):
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO posts (title, content, category, image_path)
        VALUES (?, ?, ?, ?)
    ''', (title, content, category, image_path))
    conn.commit()
    conn.close()

# Get all posts
def get_all_posts():
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, category, created_at FROM posts ORDER BY created_at DESC")
    posts = cursor.fetchall()
    conn.close()
    return posts

# Get single post
def get_post_by_id(post_id):
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute("SELECT title, content, category, image_path FROM posts WHERE id=?", (post_id,))
    post = cursor.fetchone()
    conn.close()
    return post

# Update post
def update_post(post_id, title, content, category, image_path=None):
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    if image_path:
        cursor.execute('''
            UPDATE posts
            SET title=?, content=?, category=?, image_path=?
            WHERE id=?
        ''', (title, content, category, image_path, post_id))
    else:
        cursor.execute('''
            UPDATE posts
            SET title=?, content=?, category=?
            WHERE id=?
        ''', (title, content, category, post_id))
    conn.commit()
    conn.close()

# Delete post
def delete_post(post_id):
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id=?", (post_id,))
    conn.commit()
    conn.close()

# Fetch all public blog posts
def get_published_posts():
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content, category, image_path, created_at FROM posts ORDER BY created_at DESC")
    posts = cursor.fetchall()
    conn.close()
    return posts

# Fetch single blog post
def get_full_post(post_id):
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute("SELECT title, content, category, image_path, created_at FROM posts WHERE id=?", (post_id,))
    post = cursor.fetchone()
    conn.close()
    return post

# Get all unique categories
def get_all_categories():
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM posts")
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    return categories

# Get posts by category
def get_posts_by_category(category):
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, title, content, category, image_path, created_at FROM posts WHERE category=? ORDER BY created_at DESC",
        (category,)
    )
    posts = cursor.fetchall()
    conn.close()
    return posts

# Search posts by keyword
def search_posts(keyword):
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    like_query = f"%{keyword}%"
    cursor.execute(
        "SELECT id, title, content, category, image_path, created_at FROM posts WHERE title LIKE ? OR content LIKE ? ORDER BY created_at DESC",
        (like_query, like_query)
    )
    posts = cursor.fetchall()
    conn.close()
    return posts



# --- Verify login credentials ---
def verify_user(username, password):
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result:
        stored_hash = result[0]
        return bcrypt.checkpw(password.encode(), stored_hash)
    return False
