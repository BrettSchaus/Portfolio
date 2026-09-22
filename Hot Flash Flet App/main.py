import flet as ft


def main(page: ft.Page):
    page.title = 'Increment Counter'
    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'
    page.theme_mode = ft.ThemeMode.LIGHT

    text = ft.Text(value='This is some text',
                      text_align=ft.TextAlign.CENTER,
                      width=200,
                      size=100)

    page.add(text)


if __name__ == '__main__':
    ft.run(main)


# Run "$HOME/PycharmProjects/Portfolio/Hot Flash Flet App"
# Then source .venv/bin/activate
# Then flet run main.py
# Then you can modify the code in pycharm and after saving the file, it update automatically