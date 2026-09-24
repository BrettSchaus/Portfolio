import flet as ft
import flet_audio as fta
import asyncio


def main(page: ft.Page):
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
    page.theme_mode = ft.ThemeMode.DARK

    duration = 0
    position = 0

    async def play():
        await audio.play()

    async def pause():
        await audio.pause()

    def set_volume(value: float):
        audio.volume = max(0, min(1, audio.volume + value))

    # Convert milliseconds into minutes and seconds
    def format_time(milliseconds):
        seconds = int(milliseconds / 1000)
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    # Audio duration becomes available
    def to_milliseconds(value):
        milliseconds = getattr(value, "in_milliseconds", value)

        if callable(milliseconds):
            return milliseconds()

        return int(milliseconds)

    def format_time(milliseconds):
        seconds = int(milliseconds / 1000)
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def duration_changed(e):
        nonlocal duration
        duration = to_milliseconds(e.duration)
        progress.max = duration
        remaining_time.value = format_time(duration)

        page.update()

    # Audio position changes every second while playing
    def position_changed(e):
        nonlocal position

        new_position = to_milliseconds(e.position)

        # Detect the audio looping back to the beginning
        if new_position < position:
            position = 0
            progress.value = 0
            current_time.value = "00:00"
            remaining_time.value = format_time(duration)
        else:
            position = new_position

            progress.value = position
            current_time.value = format_time(position)

            remaining = max(0, duration - position)
            remaining_time.value = f"-{format_time(remaining)}"

        page.update()

    # User finishes dragging the progress bar
    async def progress_changed(e):
        position = e.control.value

        await audio.seek(
            ft.Duration(milliseconds=position)
        )

    async def update_progress():
        while True:
            try:
                current = await audio.get_current_position()

                if current is not None:
                    position = to_milliseconds(current)

                    progress.value = position
                    current_time.value = format_time(position)

                    remaining = max(0, duration - position)
                    remaining_time.value = f"-{format_time(remaining)}"

                    page.update()

            except Exception as e:
                print("Progress update error:", e)

            await asyncio.sleep(1)

    audio = fta.Audio(
        src="Fan_noise_30min.mp3",
        autoplay=False,
        volume=1,
        balance=0,
        release_mode=fta.ReleaseMode.LOOP,
        on_loaded=lambda _: print("Loaded"),
        on_duration_change=duration_changed,
        on_state_change=lambda e: print("State changed:", e.state
        ),
    )

    page.services.append(audio)

    # Progress bar
    progress = ft.Slider(
        min=0,
        max=1,
        value=0,
        on_change_end=progress_changed,
    )

    # Time displays
    current_time = ft.Text("00:00")
    remaining_time = ft.Text("-00:00")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[

                    # Play / Pause
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.PLAY_CIRCLE,
                                on_click=play,
                                icon_color=ft.Colors.INDIGO,
                                icon_size=70,
                            ),

                            ft.IconButton(
                                icon=ft.Icons.PAUSE_CIRCLE,
                                on_click=pause,
                                icon_color=ft.Colors.INDIGO,
                                icon_size=70,
                            ),
                        ],

                        alignment=ft.MainAxisAlignment.CENTER,
                    ),

                    # Time
                    ft.Row(
                        controls=[
                            current_time,
                            ft.Text("/"),
                            remaining_time,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),

                    # Progress Bar
                    progress,

                    # Volume
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.REMOVE_CIRCLE,
                                on_click=lambda _: set_volume(-0.1),
                                icon_color=ft.Colors.INDIGO,
                                icon_size=60,
                            ),

                            ft.IconButton(
                                icon=ft.Icons.ADD_CIRCLE,
                                on_click=lambda _: set_volume(0.1),
                                icon_color=ft.Colors.INDIGO,
                                icon_size=60,
                            ),
                        ],

                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ]
            )
        )
    )
    page.run_task(update_progress)

if __name__ == "__main__":
    ft.run(main, assets_dir="assets")