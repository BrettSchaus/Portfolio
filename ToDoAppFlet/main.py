import flet as ft
import datetime
import json
import os
import asyncio

TODO_FILE = "todos.json"
COUNTER_FILE = "counters.json"


def main(page: ft.Page):
    today = datetime.datetime.now()

    todos = []

    # Load saved todos
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, "r") as file:
            todos = json.load(file)

    # Save todos
    def save_todos():
        with open(TODO_FILE, "w") as file:
            json.dump(todos, file)


    counters = []
    selected_date = None
    selected_time = None

    # Load saved counters
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "r") as file:
            counters = json.load(file)


    # Save counters
    def save_counters():
        with open(COUNTER_FILE, "w") as file:
            json.dump(counters, file)

    # Todo Input
    todo_input = ft.TextField(
        label="What do you need to do?",
        expand=True,
        on_submit=lambda e: add_todo(e)
        )

    # Counter Input
    counter_input = ft.TextField(
        label="Create a counter",
        width=300,
    )

    # DatePicker
    def handle_change(e: ft.Event[ft.DatePicker]):
        nonlocal selected_date
        selected_date = e.control.value
        print("Selected date:", selected_date)

    def handle_time_change(e):
        nonlocal selected_time
        selected_time = e.control.value
        print("Selected time:", selected_time)

    time_picker = ft.TimePicker(
        on_change=handle_time_change,
    )

    def handle_dismissal(e):
        print("DatePicker dismissed")

    picker = ft.DatePicker(
        first_date=datetime.datetime(
            year=1990,
            month=1,
            day=1
        ),
        last_date=today + datetime.timedelta(days=365),
        current_date=today,
        on_change=handle_change,
        on_dismiss=handle_dismissal,
    )


    ## Todo Functions
    # Display todos
    def show_todos():
        todo_list.controls.clear()

        for index, todo in enumerate(todos):
            checkbox = ft.Checkbox(
                label=todo["text"],
                value=todo["completed"],
                data=index,
                on_change=toggle_todo
            )

            delete_button = ft.IconButton(
                icon=ft.Icons.DELETE,
                data=index,
                on_click=delete_todo
            )

            row = ft.Row(
                controls=[
                    checkbox,
                    delete_button
                ]
            )

            todo_list.controls.append(row)

        page.update()

    # Add a todo
    def add_todo(e):
        if todo_input.value.strip() == "":
            return

        todos.append({
            "text": todo_input.value,
            "completed": False
        })

        todo_input.value = ""

        save_todos()
        show_todos()


    # Complete / incomplete todo
    def toggle_todo(e):
        index = int(e.control.data)

        todos[index]["completed"] = e.control.value

        save_todos()
        show_todos()


    # Delete a todo
    def delete_todo(e):
        index = int(e.control.data)

        def confirm_delete(e):
            todos.pop(index)
            save_todos()
            show_todos()
            page.pop_dialog()

        modal_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please confirm"),
            content=ft.Text("Do you really want to delete this task?"),
            actions=[
                ft.TextButton("Yes", on_click=confirm_delete),
                ft.TextButton("No", on_click=lambda e: page.pop_dialog()),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

        page.show_dialog(modal_dialog)

    # Delete completed todos
    def clear_completed(e):
        todos[:] = [
            todo
            for todo in todos
            if not todo["completed"]
        ]

        save_todos()
        show_todos()



    # Reorder todo list
    def reorder_todos(e):
        old_index = e.old_index
        new_index = e.new_index

        todo = todos.pop(old_index)

        todos.insert(new_index, todo)

        save_todos()
        show_todos()


    ## Counter Functions
    # Add counter
    def add_counter(e):
        if counter_input.value.strip() == "":
            return

        if selected_date is None or selected_time is None:
            return

        start_datetime = datetime.datetime.combine(
            selected_date,
            selected_time
        )

        counters.append({
            "text": counter_input.value,
            "start_date": start_datetime.isoformat()
        })

        counter_input.value = ""

        save_counters()
        show_counters()


    # Delete counter
    def delete_counter(e):
        index = int(e.control.data)

        def confirm_delete(e):
            counters.pop(index)
            save_counters()
            show_counters()
            page.pop_dialog()

        modal_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please confirm"),
            content=ft.Text("Do you really want to delete this counter?"),
            actions=[
                ft.TextButton(
                    "Yes",
                    on_click=confirm_delete
                ),
                ft.TextButton(
                    "No",
                    on_click=lambda e: page.pop_dialog()
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.show_dialog(modal_dialog)


    # Display counters
    def show_counters():
        counter_list.controls.clear()

        for index, counter in enumerate(counters):
            start_date = datetime.datetime.fromisoformat(
                counter["start_date"]
            )

            date_text = start_date.strftime("%d/%m/%Y at %H:%M")

            now = datetime.datetime.now(start_date.tzinfo)
            elapsed = now - start_date

            years = elapsed.days // 365
            days = elapsed.days % 365
            hours, remainder = divmod(elapsed.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            counter_text = ft.Text(
                f"{counter['text']} - Started: {date_text} - "
                f"Time since: {years} years, {days} days, {hours} hours, {minutes} minutes"
            )

            delete_button = ft.IconButton(
                icon=ft.Icons.DELETE,
                data=index,
                on_click=delete_counter
            )
            row = ft.Row(
                controls=[
                    counter_text,
                    delete_button
                ]
            )
            counter_list.controls.append(row)
        page.update()

    async def update_counters():
        while True:
            show_counters()
            await asyncio.sleep(1)

    # Buttons
    todo_add_button = ft.IconButton(
        icon=ft.Icons.ADD,
        on_click=add_todo
    )

    counter_add_button = ft.IconButton(
        icon=ft.Icons.ADD,
        on_click=add_counter
    )

    clear_button = ft.TextButton(
        "Clear completed",
        on_click=clear_completed
    )

    # Lists
    todo_list = ft.ReorderableListView(
        expand=True,
        on_reorder=reorder_todos,
    )

    counter_list = ft.Column()

    # Page
    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Tabs(
                selected_index=0,
                length=3,
                expand=True,

                content=ft.Column(
                    expand=True,

                    controls=[
                        # Tab Bar
                        ft.TabBar(
                            tabs=[
                                ft.Tab(label="Tab 1", icon=ft.Icons.CHECKLIST),
                                ft.Tab(label="Tab 2", icon=ft.Icons.ACCESS_ALARM),
                                ft.Tab(
                                    label=ft.CircleAvatar(
                                        foreground_image_src="https://avatars.githubusercontent.com/u/102273996?s=200&amp;v=4",
                                    ),
                                ),
                            ]
                        ),

                        # Tab Content
                        ft.TabBarView(
                            expand=True,

                            controls=[

                                # Tab 1
                                ft.Container(

                                    alignment=ft.Alignment.CENTER,

                                    content=ft.Column(

                                        horizontal_alignment=
                                        ft.CrossAxisAlignment.CENTER,

                                        controls=[

                                            ft.Text(
                                                "To Do List",
                                                size=32,
                                                weight=ft.FontWeight.BOLD
                                            ),

                                            ft.Row(
                                                controls=[
                                                    todo_input,
                                                    todo_add_button
                                                ]
                                            ),

                                            todo_list,
                                            ft.Divider(),
                                            clear_button,
                                        ],
                                    ),
                                ),

                                # Tab 2
                                ft.Container(
                                    alignment=ft.Alignment.CENTER,

                                    content=ft.Column(
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                                        controls=[
                                            ft.Text("Counters", size=32, weight=ft.FontWeight.BOLD),
                                            ft.Button(icon=ft.Icons.CALENDAR_MONTH,
                                                      on_click=lambda _: page.show_dialog(picker),
                                                      content="Pick date"),
                                            ft.Button(
                                                icon=ft.Icons.ACCESS_TIME,
                                                on_click=lambda _: page.show_dialog(time_picker),
                                                content="Pick time",
                                            ),
                                            ft.Row(
                                                alignment=ft.MainAxisAlignment.CENTER,
                                                controls=[
                                                    counter_input,
                                                    counter_add_button
                                                ]
                                            ),
                                            counter_list,
                                        ],
                                    ),
                                ),
                                # Tab 3
                                ft.Container(
                                    alignment=ft.Alignment.CENTER,
                                    content=ft.Text("This is Tab 3"),
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        )
    )
    # Show saved data when app starts
    show_todos()
    show_counters()

    # Start counter refresh
    page.run_task(update_counters)

if __name__ == "__main__":
    ft.run(main)