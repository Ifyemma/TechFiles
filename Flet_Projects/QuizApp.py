import flet as ft

questions = [
    {"q": "What is the capital of France?", "a": ["Paris", "Berlin", "Rome"], "c": 0},
    {"q": "2 + 2 = ?", "a": ["3", "4", "5"], "c": 1}
]

def main(page: ft.Page):
    index = 0
    score = 0
    question_text = ft.Text()
    options = ft.Column()
    result_text = ft.Text()

    def show_question():
        if index < len(questions):
            q = questions[index]
            question_text.value = q["q"]
            options.controls.clear()
            for i, ans in enumerate(q["a"]):
                options.controls.append(
                    ft.ElevatedButton(ans, on_click=lambda e, i=i: check_answer(i))
                )
            page.update()
        else:
            question_text.value = f"Quiz Over! Score: {score}/{len(questions)}"
            options.controls.clear()
            page.update()

    def check_answer(i):
        nonlocal index, score
        if i == questions[index]["c"]:
            score += 1
        index += 1
        show_question()

    page.add(question_text, options, result_text)
    show_question()

ft.app(target=main)
