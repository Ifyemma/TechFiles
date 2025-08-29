import flet as ft

def main(page: ft.Page):
    image_column = ft.Column()

    def upload_files(e: ft.FilePickerResultEvent):
        for file in e.files:
            image_column.controls.append(
                ft.Image(src=file.path, width=200, height=200, fit="contain")
            )
        page.update()

    file_picker = ft.FilePicker(on_result=upload_files)
    page.overlay.append(file_picker)

    page.add(
        ft.ElevatedButton("Upload Image", on_click=lambda _: file_picker.pick_files(allow_multiple=True)),
        image_column
    )

ft.app(target=main)
