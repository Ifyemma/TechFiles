import flet as ft
from db import init_db, verify_user
from db import save_post
from db import get_all_posts, delete_post
from db import get_post_by_id, update_post
from db import get_published_posts, get_full_post
from db import get_all_categories, get_posts_by_category, search_posts
from db import init_db
import os
import time



# --- Page Routing ---
def route_change(route):
    page.views.clear()

    if route == "/":
        page.views.append(public_home_view(page))
    elif route == "/admin/login":
        page.views.append(admin_login_view(page))
    elif route == "/admin/dashboard":
        page.views.append(admin_dashboard_view(page))
    elif route == "/admin/add-post":
        page.views.append(add_post_view(page))
    elif route.startswith("/admin/edit-post/"):
        post_id = int(route.split("/")[-1])
        page.views.append(edit_post_view(page, post_id))
    elif route.startswith("/post/"):
        post_id = int(route.split("/")[-1])
        page.views.append(public_post_view(page, post_id))
    else:
        page.views.append(not_found_view(page))

    page.update()

# --- Home View ---
def home_view(page):
    return ft.View(
        route="/",
        controls=[
            ft.Text("Welcome to Blog CMS!", size=30),
            ft.ElevatedButton("Go to Admin Login", on_click=lambda _: page.go("/admin/login"))
        ]
    )

# --- Admin Login View ---
def admin_login_view(page):
    return ft.View(
        route="/admin/login",
        controls=[
            ft.Text("Admin Login", size=25),
            ft.TextField(label="Username"),
            ft.TextField(label="Password", password=True),
            ft.ElevatedButton("Login", on_click=lambda _: page.go("/admin/dashboard"))
        ]
    )

# --- Admin Dashboard View ---
def admin_dashboard_view(page):
    user = page.client_storage.get("user")
    if not user:
        page.go("/admin/login")
        return ft.View(route="/admin/dashboard", controls=[])

    posts = get_all_posts()
    post_cards = []

    for post in posts:
        post_id, title, category, created = post
        post_cards.append(
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(f"📝 {title}", size=20, weight="bold"),
                        ft.Text(f"📂 {category} | 🕒 {created}"),
                        ft.Row([
                            ft.ElevatedButton("Edit", on_click=lambda e, pid=post_id: page.go(f"/admin/edit-post/{pid}")),
                            ft.ElevatedButton("Delete", on_click=lambda e, pid=post_id: handle_delete(page, pid), bgcolor="red", color="white")
                        ])
                    ]),
                    padding=10
                )
            )
        )

    def handle_delete(page, pid):
        delete_post(pid)
        page.go("/admin/dashboard")  # Refresh

    return ft.View(
        route="/admin/dashboard",
        controls=[
            ft.Text(f"Welcome, {user}", size=25),
            ft.ElevatedButton("➕ Add New Post", on_click=lambda _: page.go("/admin/add-post")),
            ft.ElevatedButton("🔓 Logout", on_click=lambda _: (page.client_storage.clear(), page.go("/"))),
            ft.Column(post_cards)
        ]
    )

# Optional
'''def admin_dashboard_view(page):
    user = page.client_storage.get("user")
    if not user:
        page.go("/admin/login")
        return ft.View(route="/admin/dashboard", controls=[])
    
    return ft.View(
        route="/admin/dashboard",
        controls=[
            ft.Text(f"Welcome, {user}!", size=25),
            ft.ElevatedButton("Logout", on_click=lambda _: (
                page.client_storage.clear(),
                page.go("/")
            ))
        ]
    )
'''

# --- Not Found View ---
def not_found_view(page):
    return ft.View(
        route=page.route,
        controls=[
            ft.Text("404 - Page not found", size=25),
            ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/"))
        ]
    )

def add_post_view(page):
    if not page.client_storage.get("user"):
        page.go("/admin/login")
        return ft.View(route="/admin/add-post", controls=[])
    
    # Added
    if not title.value or not content.value:
        status.value = "❌ Title and content are required."
        page.update()
        return

    title = ft.TextField(label="Title", width=400)
    content = ft.TextField(label="Content", multiline=True, min_lines=5, width=400)
    category = ft.TextField(label="Category", width=400)
    image = ft.FilePicker()
    image_result = ft.Text("No image selected", italic=True)
    status = ft.Text("", color="green")

    def handle_upload(e: ft.FilePickerResultEvent):
        if e.files:
            picked = e.files[0]
            new_path = f"assets/uploads/{int(time.time())}_{picked.name}"
            os.makedirs("assets/uploads", exist_ok=True)
            with open(new_path, "wb") as f:
                f.write(picked.read_bytes())
            image_result.value = new_path
            page.update()

    image.on_result = handle_upload

    def submit_post(e):
        if title.value and content.value:
            save_post(title.value, content.value, category.value, image_result.value)
            status.value = "✅ Post saved successfully!"
            title.value = content.value = category.value = ""
            image_result.value = "No image selected"
            page.update()
        else:
            status.value = "❌ Title and Content required"
            page.update()

    return ft.View(
        route="/admin/add-post",
        controls=[
            ft.Text("Add New Blog Post", size=25),
            title,
            content,
            category,
            ft.ElevatedButton("Pick Image", on_click=lambda _: image.pick_files()),
            image_result,
            ft.ElevatedButton("Submit", on_click=submit_post),
            image,
            status,
            ft.ElevatedButton("← Back to Dashboard", on_click=lambda _: page.go("/admin/dashboard"))
        ]
    )

def edit_post_view(page, post_id):
    if not page.client_storage.get("user"):
        page.go("/admin/login")
        return ft.View(route="/admin/edit-post", controls=[])

    post = get_post_by_id(post_id)
    if not post:
        return ft.View(route="/admin/edit-post", controls=[ft.Text("Post not found!")])

    title = ft.TextField(label="Title", value=post[0], width=400)
    content = ft.TextField(label="Content", value=post[1], multiline=True, min_lines=5, width=400)
    category = ft.TextField(label="Category", value=post[2], width=400)
    image_path = post[3]

    image_picker = ft.FilePicker()
    image_result = ft.Text(image_path or "No image selected", italic=True)
    status = ft.Text("", color="green")

    def handle_upload(e: ft.FilePickerResultEvent):
        if e.files:
            picked = e.files[0]
            new_path = f"assets/uploads/{int(time.time())}_{picked.name}"
            os.makedirs("assets/uploads", exist_ok=True)
            with open(new_path, "wb") as f:
                f.write(picked.read_bytes())
            image_result.value = new_path
            page.update()

    image_picker.on_result = handle_upload

    def handle_update(e):
        update_post(post_id, title.value, content.value, category.value,
                    image_result.value if image_result.value != image_path else None)
        status.value = "✅ Post updated!"
        page.update()

    return ft.View(
        route=f"/admin/edit-post/{post_id}",
        controls=[
            ft.Text("Edit Blog Post", size=25),
            title,
            content,
            category,
            ft.ElevatedButton("Replace Image", on_click=lambda _: image_picker.pick_files()),
            image_result,
            ft.ElevatedButton("Update Post", on_click=handle_update),
            image_picker,
            status,
            ft.ElevatedButton("← Back to Dashboard", on_click=lambda _: page.go("/admin/dashboard"))
        ]
    )

def public_home_view(page):
    search_field = ft.TextField(label="🔍 Search blog...", width=300)
    category_dropdown = ft.Dropdown(label="Filter by Category", width=300)

    post_column = ft.Column()

    def load_posts(posts):
        post_column.controls.clear()
        for post in posts:
            post_id, title, content, category, image, created = post
            preview = content[:100] + "..." if len(content) > 100 else content

            post_column.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(title, size=20, weight="bold", text_align = "center"),
                            ft.Text(f"📂 {category} | 🕒 {created}", italic=True),
                            ft.Text(preview),
                            ft.ElevatedButton("Read More", on_click=lambda e, pid=post_id: page.go(f"/post/{pid}"))
                        ]),
                        padding=15,
                        border_radius=10,
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        margin=ft.margin.only(bottom=10)

                    )
                )
            )
        page.update()

    def handle_search(e):
        keyword = search_field.value.strip()
        if keyword:
            posts = search_posts(keyword)
        else:
            posts = get_published_posts()
        load_posts(posts)

    def handle_category_change(e):
        selected = category_dropdown.value
        if selected == "All":
            load_posts(get_published_posts())
        else:
            load_posts(get_posts_by_category(selected))

    # Populate categories
    all_categories = get_all_categories()
    category_dropdown.options = [ft.dropdown.Option("All")] + [
        ft.dropdown.Option(cat) for cat in all_categories
    ]
    category_dropdown.value = "All"
    category_dropdown.on_change = handle_category_change

    search_button = ft.ElevatedButton("Search", on_click=handle_search)

    # Initial load
    load_posts(get_published_posts())

    return ft.View(
        route="/",
        controls=[
            ft.Text("📰 Public Blog Page", size=30),
            ft.Row([search_field, search_button]),
            ft.Row([category_dropdown]),
            post_column,
            ft.ElevatedButton("🔐 Admin Login", on_click=lambda _: page.go("/admin/login"))
        ]
    )


def public_post_view(page, post_id):
    post = get_full_post(post_id)
    if not post:
        return ft.View(route="/post", controls=[ft.Text("Post not found!")])

    title, content, category, image, created = post

    image_control = ft.Image(src=image, width=300) if image else ft.Text("")

    return ft.View(
        route=f"/post/{post_id}",
        controls=[
            ft.Text(title, size=25, weight="bold"),
            ft.Text(f"📂 {category} | 🕒 {created}", italic=True),
            image_control,
            ft.Text(content),
            ft.ElevatedButton("← Back to Home", on_click=lambda _: page.go("/"))
        ]
    )



# --- Main App ---
def main(page: ft.Page):
    init_db()
    page.title = "Flet Blog CMS"
    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)
#ft.app(target=main, view=ft.WEB_BROWSER)

