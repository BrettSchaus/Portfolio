import flet as ft
import json
import os

FILE_NAME = "tasks.json"


def main(page: ft.Page):
    # Page settings
    page.title = "My Todo List"
    page.padding = 20

    # Load saved tasks
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            tasks = json.load(file)
    else:
        tasks = []

    # Save tasks
    def save_tasks():
        with open(FILE_NAME, "w") as file:
            json.dump(tasks, file)

    # Add a task
    def add_task(e):

        if task_input.value.strip() == "":
            return

        tasks.append({
            "text": task_input.value,
            "completed": False
        })

        task_input.value = ""

        save_tasks()
        show_tasks()

    # Complete / uncomplete
    def toggle_task(e):

        index = int(e.control.data)

        tasks[index]["completed"] = e.control.value

        save_tasks()
        show_tasks()

    # Delete a task
    def delete_task(e):

        index = int(e.control.data)

        def confirm_delete(e):
            tasks.pop(index)
            save_tasks()
            show_tasks()
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

    # Delete completed tasks
    def clear_completed(e):

        tasks[:] = [
            task for task in tasks
            if not task["completed"]
        ]

        save_tasks()
        show_tasks()

    def show_tasks():

        task_list.controls.clear()

        for index, task in enumerate(tasks):
            checkbox = ft.Checkbox(
                label=task["text"],
                value=task["completed"],
                data=index,
                on_change=toggle_task,
                expand=True
            )

            delete_button = ft.IconButton(
                icon=ft.Icons.DELETE,
                data=index,
                on_click=delete_task
            )

            row = ft.Row(
                controls=[
                    checkbox,
                    delete_button
                ]
            )

            task_list.controls.append(row)

        page.update()

    # Input box
    task_input = ft.TextField(
        label="What do you need to do?",
        expand=True,
        on_submit=add_task
    )

    # Add button
    add_button = ft.IconButton(
        icon=ft.Icons.ADD,
        on_click=add_task
    )

    # List of tasks
    task_list = ft.Column()

    # Clear completed button
    clear_button = ft.TextButton(
        "Clear completed",
        on_click=clear_completed
    )

    # Build the page
    page.add(

        ft.Text(
            "My Todo List",
            size=32,
            weight=ft.FontWeight.BOLD
        ),

        ft.Row(
            controls=[
                task_input,
                add_button
            ]
        ),

        task_list,

        ft.Divider(),
        clear_button
    )

    # Show saved tasks
    show_tasks()


ft.run(main)
