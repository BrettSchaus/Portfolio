import flet as ft


def main(page: ft.Page):
    page.title = 'Increment Counter'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT  # Dark mode or light mode

    text_number = ft.TextField(value='0', text_align=ft.TextAlign.RIGHT, width=100)

    def decrement(e: ft.Event):
        text_number.value = str(int(text_number.value) - 1)
        page.update()

    def increment(e: ft.Event):
        text_number.value = str(int(text_number.value) + 1)
        page.update()


    page.add(
        ft.Row(
            [ft.IconButton(icon=ft.Icons.REMOVE, on_click=decrement),
             text_number,
             ft.IconButton(icon=ft.Icons.ADD, on_click=increment)],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

if __name__ == '__main__':
    ft.run(main)  # Can add -> view=ft.AppView.WEB_BROWSER to launch this app in a web browser