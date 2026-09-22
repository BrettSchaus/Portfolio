import flet as ft
from flet import Page, Row, Text, KeyboardEvent


def main(page: Page):
    page.title = 'Keyboard PRO'
    page.spacing = 30
    page.vertical_alignment = 'center'
    page.horizontal_alignment = 'center'

    # Creating the text views
    key: Text = Text(value='Key', size = 30)
    shift: Text = Text(value='Shift', size = 30, color = 'red')
    ctrl: Text = Text(value='Ctrl', size = 30, color = 'blue')
    alt: Text = Text(value='Alt', size = 30, color = 'green')
    meta: Text = Text(value='Meta', size = 30, color = 'yellow')

    # Handling the keyboard events
    def on_keyboard(e: KeyboardEvent):  # Possibly need -> None beside the :
        key.value = e.key
        shift.visible = e.shift
        ctrl.visible = e.ctrl
        alt.visible = e.alt
        meta.visible = e.meta
        print(e.data)
        page.update()

    # Linking the keyboard events to the page
    page.on_keyboard_event = on_keyboard

    # Creating our basic page
    page.add(
        Text('Press any combination of keys...'),
            Row(controls=[key, shift, ctrl, alt, meta],
        alignment=ft.MainAxisAlignment.CENTER)
    )

if __name__ == '__main__':
    ft.run(main)