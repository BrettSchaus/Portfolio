import flet as ft
import datetime
import json
import os

DATA_FILE = "caffeine_tracker.json"


def main(page: ft.Page):
    page.title = "Caffeine Tracker"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 10

    caffeine_intakes = []
    daily_limit = 200

    # Load data
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                data = json.load(file)

                caffeine_intakes = data.get(
                    "caffeine_intakes", []
                )

                daily_limit = data.get(
                    "daily_limit", 200
                )

        except (json.JSONDecodeError, OSError):
            caffeine_intakes = []
            daily_limit = 200

    # Save data
    def save_data():
        data = {
            "daily_limit": daily_limit,
            "caffeine_intakes": caffeine_intakes,
        }

        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)

    # Home page controls
    total_text = ft.Text(
        "Today's caffeine: 0 mg",
        size=24,
        weight=ft.FontWeight.BOLD,
    )

    percentage_text = ft.Text(
        "0%",
        size=18,
        weight=ft.FontWeight.BOLD,
    )

    progress_ring = ft.ProgressRing(
        value=0,
        width=120,
        height=120,
    )

    progress_stack = ft.Stack(
        width=120,
        height=120,
        controls=[
            ft.Container(
                content=percentage_text,
                alignment=ft.Alignment.CENTER,
                width=120,
                height=120,
            ),
            progress_ring,
        ],
    )

    daily_limit_text = ft.Text(
        f"Daily limit: {daily_limit} mg",
        size=16,
    )

    # Input controls
    caffeine_intake_input = ft.TextField(
        label="What did you drink?",
        hint_text="e.g. Coffee",
        expand=True,
    )

    caffeine_amount_input = ft.TextField(
        label="Caffeine",
        hint_text="mg",
        width=120,
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    # History page
    history_list = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    # Calculating today's total
    def get_today_total():
        today = datetime.date.today()

        total = 0

        for intake in caffeine_intakes:
            try:
                intake_time = datetime.datetime.fromisoformat(
                    intake["timestamp"]
                )

                if intake_time.date() == today:
                    total += intake["amount_mg"]

            except (KeyError, ValueError, TypeError):
                continue

        return total

    # Updating homepage
    def update_home():
        today_total = get_today_total()

        total_text.value = (
            f"Today's caffeine: {today_total} mg"
        )

        if daily_limit > 0:
            progress = today_total / daily_limit
        else:
            progress = 0

        # Never let the ring go above 100%
        progress = min(progress, 1.0)

        percentage = int(progress * 100)

        progress_ring.value = progress
        percentage_text.value = f"{percentage}%"

        daily_limit_text.value = (
            f"Daily limit: {daily_limit} mg"
        )

    # Display history
    def show_history():
        history_list.controls.clear()

        if not caffeine_intakes:

            history_list.controls.append(
                ft.Container(
                    content=ft.Text(
                        "No caffeine recorded yet.",
                        size=18,
                    ),
                    padding=20,
                )
            )

        else:

            # Newest entries first
            for index in reversed(
                range(len(caffeine_intakes))
            ):

                intake = caffeine_intakes[index]

                try:
                    intake_time = (
                        datetime.datetime.fromisoformat(
                            intake["timestamp"]
                        )
                    )
                except (KeyError, ValueError):
                    continue

                caffeine_text = ft.Text(
                    f'{intake["drink"]} — '
                    f'{intake["amount_mg"]} mg\n'
                    f'{intake_time.strftime("%d/%m/%Y %H:%M")}',
                    expand=True,
                )

                delete_button = ft.IconButton(
                    icon=ft.Icons.DELETE,
                    tooltip="Delete",
                    data=index,
                    on_click=delete_caffeine_intake,
                )

                history_list.controls.append(
                    ft.Row(
                        controls=[
                            caffeine_text,
                            delete_button,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    )
                )

    # Delete entries
    def delete_caffeine_intake(e):
        index = e.control.data

        caffeine_intakes.pop(index)

        save_data()

        update_home()
        show_history()

        page.update()

    # Adding entries
    def add_caffeine_intake(e):
        drink = caffeine_intake_input.value.strip()
        amount = caffeine_amount_input.value.strip()

        if drink == "":
            return

        if amount == "":
            return

        try:
            amount_mg = int(amount)

            if amount_mg < 0:
                return

        except ValueError:
            return

        caffeine_intakes.append(
            {
                "drink": drink,
                "amount_mg": amount_mg,
                "timestamp": (datetime.datetime.now().isoformat()),
            }
        )

        caffeine_intake_input.value = ""
        caffeine_amount_input.value = ""

        save_data()

        update_home()
        show_history()

        page.update()

    def quick_add():
        caffeine_intakes.append(
            {
                "drink": "Espresso",
                "amount_mg": 60,
                "timestamp": (datetime.datetime.now().isoformat()),
            }
        )
        save_data()

        update_home()
        show_history()

        page.update()

    # Daily limit in setting page
    limit_input = ft.TextField(
        label="Daily caffeine limit",
        hint_text="e.g. 200",
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    def close_limit_dialog(e):
        limit_dialog.open = False
        page.update()

    def save_new_limit(e):
        nonlocal daily_limit

        try:
            new_limit = int(limit_input.value)

            if new_limit <= 0:
                return

            daily_limit = new_limit

            save_data()
            update_home()

            limit_dialog.open = False

            page.update()

        except (ValueError, TypeError):
            return

    limit_dialog = ft.AlertDialog(
        title=ft.Text(
            "Set Daily Caffeine Limit"
        ),
        content=limit_input,
        actions=[
            ft.TextButton(
                "Cancel",
                on_click=close_limit_dialog,
            ),
            ft.TextButton(
                "Save",
                on_click=save_new_limit,
            ),
        ],
    )

    def open_limit_dialog(e):
        limit_input.value = str(daily_limit)

        limit_dialog.open = True

        page.update()

    # Add new caffeine intake button
    caffeine_intake_add_button = ft.IconButton(
        icon=ft.Icons.ADD,
        tooltip="Add caffeine intake",
        on_click=add_caffeine_intake,
    )

    # Home view
    home_view = ft.Column(
        expand=True,
        controls=[
            ft.Text(
                "Caffeine Tracker",
                size=32,
                weight=ft.FontWeight.BOLD,
            ),

            total_text,

            ft.Container(
                content=progress_stack,
                alignment=ft.Alignment.CENTER,
                padding=20,
            ),

            ft.Container(
                content=daily_limit_text,
                alignment=ft.Alignment.CENTER,
            ),

            ft.Container(
                content=ft.Button(
                    "Set Daily Limit",
                    icon=ft.Icons.SETTINGS,
                    on_click=open_limit_dialog,
                ),
                alignment=ft.Alignment.CENTER,
                padding=10,
            ),

            ft.Divider(),

            ft.Text(
                "Add Caffeine Intake",
                size=20,
                weight=ft.FontWeight.BOLD,
            ),

            ft.Row(
                controls=[
                    caffeine_intake_input,
                    caffeine_amount_input,
                    caffeine_intake_add_button,
                ],
            ),
            ft.IconButton(
                icon=ft.Icons.ADD_CIRCLE,
                on_click=quick_add,
                icon_color=ft.Colors.INDIGO,
                icon_size=70,
            ),
        ],
    )

    # History view
    history_view = ft.Column(
        expand=True,
        controls=[
            ft.Text(
                "Caffeine History",
                size=32,
                weight=ft.FontWeight.BOLD,
            ),
            ft.Divider(),
            history_list,
        ],
    )

    # Settings view
    settings_view = ft.Column(
        expand=True,
        controls=[
            ft.Text(
                "Settings",
                size=32,
                weight=ft.FontWeight.BOLD,
            ),

            ft.Divider(),

            ft.Text(
                "Daily Caffeine Limit",
                size=20,
                weight=ft.FontWeight.BOLD,
            ),

            daily_limit_text,

            ft.Button(
                "Change Daily Limit",
                icon=ft.Icons.EDIT,
                on_click=open_limit_dialog,
            ),
        ],
    )

    # Content switcher
    content = ft.Container(
        expand=True,
        content=home_view,
    )

    def show_home(e=None):
        content.content = home_view
        update_home()
        page.update()

    def show_history_tab(e=None):
        show_history()
        content.content = history_view
        page.update()

    def show_settings(e=None):
        content.content = settings_view
        page.update()


    # Bottom navigation
    bottom_bar = ft.BottomAppBar(
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                ft.IconButton(
                    icon=ft.Icons.HOME,
                    tooltip="Home",
                    on_click=show_home,
                ),

                ft.IconButton(
                    icon=ft.Icons.HISTORY,
                    tooltip="History",
                    on_click=show_history_tab,
                ),

                ft.IconButton(
                    icon=ft.Icons.SETTINGS,
                    tooltip="Settings",
                    on_click=show_settings,
                ),
            ],
        ),
    )

    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    content,
                    bottom_bar,
                ],
            ),
        )
    )

    # Initial update
    update_home()
    show_history()


if __name__ == "__main__":
    ft.run(main)