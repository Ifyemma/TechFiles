import flet as ft

students = []

def main(page: ft.Page):
    name_input = ft.TextField(label="Student Name")
    grade_input = ft.TextField(label="Grade")
    table = ft.Column()

    def add_student(e):
        try:
            grade = float(grade_input.value)
            students.append((name_input.value, grade))
            name_input.value = ""
            grade_input.value = ""
            update_table()
        except ValueError:
            pass

    def update_table():
        table.controls.clear()
        for name, grade in students:
            table.controls.append(ft.Text(f"{name}: {grade}"))
        page.update()

    page.add(
        ft.Text("Student Grades", style="headlineSmall"),
        name_input, grade_input,
        ft.ElevatedButton("Add", on_click=add_student),
        ft.Divider(), table
    )

ft.app(target=main)
