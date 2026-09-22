import flet as ft


def main(page: ft.Page):
    page.title = 'Signup'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT

    page.window.width = 400
    page.window.height = 400
    page.window.resizable = False

    # Setup our fields
    text_username = ft.TextField(label='Username', width=200)
    text_password = ft.TextField(label='Password', width=200, password=True)
    checkbox_signup = ft.Checkbox(label='Agree to terms and conditions', value=False)
    button_submit = ft.Button(content='Sign up', width=200, disabled=True)

    def validate(e: ft.Event):
        if all([text_username.value, text_password.value, checkbox_signup.value]):
            button_submit.disabled = False
        else:
            button_submit.disabled = True

        page.update()  # Must do this to see changes on screen

    def submit(e: ft.Event):
        print('Username:', text_username.value)
        print('Password:', text_password.value)

        page.clean()

        page.add(
            ft.Row(
                controls=[
                    ft.Text(
                        value=f"Welcome: {text_username.value}!",
                        size=20,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )

    # Connect events
    checkbox_signup.on_change = validate
    text_username.on_change = validate
    text_password.on_change = validate
    button_submit.on_click = submit

    # Render the page sign-up page
    page.add(
        ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        text_username,
                        text_password,
                        checkbox_signup,
                        button_submit
                    ]
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

if __name__ == '__main__':
    ft.run(main)
