import flet as ft
import datetime
import json
import os
import asyncio

TODO_FILE = "todos.json"
COUNTER_FILE = "counters.json"
BOOKS_FILE = "books.json"

os.environ["FLET_WS_MAX_MESSAGE_SIZE"] = "8000000"  # For tab 5 grid view

# For search bar tab 4
colors = [
    "Amber",
    "Blue Grey",
    "Brown",
    "Deep Orange",
    "Green",
    "Light Blue",
    "Orange",
    "Red",
]

def main(page: ft.Page):
    ### Test for tab 5 - grid view
    r = ft.Row(wrap=True, scroll="always", expand=True)

    for i in range(100):
        r.controls.append(
            ft.Container(
                content=ft.Text(f"Item {i}"),
                width=100,
                height=100,
                alignment=ft.Alignment.CENTER,
                bgcolor=ft.Colors.AMBER_100,
                border=ft.Border.all(1, ft.Colors.AMBER_400),
                border_radius=ft.BorderRadius.all(5),
            )
        )

    ### Test for search bar in tab 4
    def build_tiles(items: list[str]) -> list[ft.Control]:
        return [
            ft.ListTile(
                title=ft.Text(item),
                data=item,
                on_click=handle_tile_click,
            )
            for item in items
        ]

    async def handle_tile_click(e: ft.Event[ft.ListTile]):
        await anchor.close_view()

    async def handle_change_search(e: ft.Event[ft.SearchBar]):
        query = e.control.value.strip().lower()
        matching = (
            [color for color in colors if query in color.lower()] if query else colors
        )
        anchor.controls = build_tiles(matching)

    def handle_submit(e: ft.Event[ft.SearchBar]):
        print(f"Submit: {e.data}")

    async def handle_tap(e: ft.Event[ft.SearchBar]):
        await anchor.open_view()

    anchor = ft.SearchBar(
        view_elevation=4,
        divider_color=ft.Colors.AMBER,
        bar_hint_text="Search colors...",
        view_hint_text="Choose a color from the suggestions...",
        on_change=handle_change_search,
        on_submit=handle_submit,
        on_tap=handle_tap,
        controls=build_tiles(colors),
    )

    ### Begin without search bar
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

    books = []
    saved_date = None

    # Load saved books
    if os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, "r") as file:
            books = json.load(file)

    # Save counters
    def save_books():
        with open(BOOKS_FILE, "w") as file:
            json.dump(books, file)

    # Todo Input
    todo_input = ft.TextField(
        label="What do you need to do?",
        expand=True,
        on_submit=lambda e: add_todo(e)
    )

    # Book Input
    book_input = ft.TextField(
        label="Which book have you finished reading?",
        expand=True,
        on_submit=lambda e: add_book(e)
    )
    # Counter Input
    counter_input = ft.TextField(
        label="Create a counter",
        width=300,
    )

    # DatePicker
    def handle_change(e: ft.Event[ft.DatePicker]):
        nonlocal selected_date

        value = e.control.value

        # Convert the DatePicker value to local time before getting the date
        local_value = value.astimezone()

        selected_date = local_value.date()

        print("Raw DatePicker value:", value)
        print("Local DatePicker value:", local_value)
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

    ## Book Functions
    # Display books
    def show_books():
        book_list.controls.clear()

        for index, book in enumerate(books):
            start_date = datetime.datetime.fromisoformat(
                book["finished_date"]
            )

            date_text = start_date.strftime("%d/%m/%Y")

            book_text = ft.Text(
                f"{book['text']} - Finished: {date_text} ",
                expand=True,
            )

            delete_button = ft.IconButton(
                icon=ft.Icons.DELETE,
                data=index,
                on_click=delete_book
            )
            row = ft.Row(
                controls=[
                    ft.Container(
                        content=book_text,
                        expand=True,
                    ),
                    delete_button,
                ],
            )
            book_list.controls.append(row)

        page.update()

    async def update_books():
        while True:
            show_books()
            await asyncio.sleep(1)

    # Add a book
    def add_book(e):
        if book_input.value.strip() == "":
            return

        books.append({
            "text": book_input.value,
            "finished_date": datetime.datetime.now().date().isoformat()
        })
        book_input.value = ""

        save_books()
        show_books()

    # Delete a book
    def delete_book(e):
        index = int(e.control.data)

        def confirm_delete(e):
            books.pop(index)
            save_books()
            show_books()
            page.pop_dialog()

        modal_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please confirm"),
            content=ft.Text("Do you really want to delete this book?"),
            actions=[
                ft.TextButton("Yes", on_click=confirm_delete),
                ft.TextButton("No", on_click=lambda e: page.pop_dialog()),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

        page.show_dialog(modal_dialog)

    ## Todo Functions
    # Display todos
    def show_todos():
        todo_list.controls.clear()
        completed_list.controls.clear()

        for index, todo in enumerate(todos):
            checkbox = ft.Checkbox(
                value=todo["completed"],
                data=index,
                on_change=toggle_todo
            )

            todo_text = ft.Text(
                todo["text"],
                expand=True,
            )

            # If completed, make it grey and crossed out
            if todo["completed"]:
                todo_text.color = ft.Colors.GREY
                todo_text.style = ft.TextStyle(
                    decoration=ft.TextDecoration.LINE_THROUGH
                )

            row = ft.Row(
                controls=[
                    checkbox,
                    ft.Container(
                        content=todo_text,
                        expand=True,
                    ),
                ],
                width=float("inf"),
            )

            # Put completed tasks below the divider
            if todo["completed"]:
                completed_list.controls.append(row)

            # Put active tasks above the divider
            else:
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

            # Get current local time
            now = datetime.datetime.now()

            elapsed = now - start_date

            total_seconds = int(elapsed.total_seconds())

            years = total_seconds // (365 * 24 * 60 * 60)
            remaining = total_seconds % (365 * 24 * 60 * 60)

            days = remaining // (24 * 60 * 60)
            remaining %= (24 * 60 * 60)

            hours = remaining // (60 * 60)
            remaining %= (60 * 60)

            minutes = remaining // 60

            counter_text = ft.Text(
                f"{counter['text']} - Started: {date_text} - "
                f"Time since: {years} years, {days} days, "
                f"{hours} hours, {minutes} minutes",
                expand=True,
            )
            delete_button = ft.IconButton(
                icon=ft.Icons.DELETE,
                data=index,
                on_click=delete_counter
            )
            row = ft.Row(
                controls=[
                    ft.Container(
                        content=counter_text,
                        expand=True,
                    ),
                    delete_button,
                ],
            )
            counter_list.controls.append(row)

        page.update()

    async def update_counters():
        while True:
            show_counters()
            await asyncio.sleep(1)

    # Buttons
    book_add_button = ft.IconButton(
        icon=ft.Icons.ADD,
        on_click=add_book
    )

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

    completed_list = ft.Column(
        expand=True,
    )

    book_list = ft.Column()
    counter_list = ft.Column()

    # Page
    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Tabs(
                selected_index=0,
                length=6,
                expand=True,

                content=ft.Column(
                    expand=True,

                    controls=[
                        # Tab Bar
                        ft.TabBar(
                            tabs=[
                                ft.Tab(label="Tab 1", icon=ft.Icons.CHECKLIST),
                                ft.Tab(label="Tab 2", icon=ft.Icons.ACCESS_ALARM),
                                ft.Tab(label="Tab 3", icon=ft.Icons.BOOK),
                                ft.Tab(label="Tab 4", icon=ft.Image(src="assets/film.png",
                                        width=24,
                                        height=24,
                                    ),
                                ),
                                ft.Tab(label="Tab 5", icon=ft.Icons.ADD_TO_QUEUE),
                                ft.Tab(label="Tab 6", icon=ft.Icons.ALL_INCLUSIVE),
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
                                            # Active Tasks
                                            todo_list,
                                            # Divider between active and completed
                                            ft.Divider(),

                                            # Completed tasks
                                            completed_list,
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
                                    content=ft.Column(
                                        horizontal_alignment=
                                        ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            ft.Text(
                                                "Finished Book List",
                                                size=32,
                                                weight=ft.FontWeight.BOLD
                                            ),
                                            ft.Row(
                                                controls=[
                                                    book_input,
                                                    book_add_button
                                                ]
                                            ),
                                            book_list,
                                        ],
                                    ),
                                ),
                                # Tab 4
                                ft.Container(
                                    bgcolor="yellow",
                                    alignment=ft.Alignment.CENTER,
                                    content=ft.Column(
                                        horizontal_alignment=
                                        ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            ft.Text(
                                                "This is tab 4",
                                                size=32,
                                                weight=ft.FontWeight.BOLD
                                            ),
                                            anchor,
                                        ],
                                    ),
                                ),
                                # Tab 5
                                ft.Container(
                                    bgcolor="red",
                                    alignment=ft.Alignment.CENTER,

                                    content=ft.Column(

                                        horizontal_alignment=
                                        ft.CrossAxisAlignment.CENTER,

                                        controls=[

                                            ft.Text(
                                                "This is tab 5",
                                                size=32,
                                                weight=ft.FontWeight.BOLD
                                            ),
                                            r,
                                        ],
                                    ),
                                ),
                                # Tab 6
                                ft.Container(
                                    bgcolor="purple",
                                    alignment=ft.Alignment.CENTER,

                                    content=ft.Column(

                                        horizontal_alignment=
                                        ft.CrossAxisAlignment.CENTER,

                                        controls=[

                                            ft.Text(
                                                "This is tab 6",
                                                size=32,
                                                weight=ft.FontWeight.BOLD
                                            ),
                                        ],
                                    ),
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
    show_books()

    # Start counter refresh
    page.run_task(update_counters)
    page.run_task(update_books)

if __name__ == "__main__":
    ft.run(main)