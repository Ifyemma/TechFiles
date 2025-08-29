import flet as ft
import openai

openai.api_key = "YOUR_OPENAI_API_KEY"

def main(page: ft.Page):
    page.title = "AI Doctor"

    chat_history = ft.Column(expand=True)
    user_input = ft.TextField(hint_text="Enter symptoms or questions...", expand=True)

    def send_message(e):
        user_text = user_input.value.strip()
        if not user_text:
            return
        chat_history.controls.append(ft.Text(f"You: {user_text}"))
        user_input.value = ""
        page.update()

        # Call OpenAI API for AI response
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_text}]
        )
        answer = response.choices[0].message.content.strip()
        chat_history.controls.append(ft.Text(f"AI Doctor: {answer}"))
        page.update()

    send_button = ft.IconButton(icon=ft.icons.SEND, on_click=send_message)

    page.add(
        chat_history,
        ft.Row([user_input, send_button])
    )

ft.app(target=main)
